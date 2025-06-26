package at.a1ta.cuco.core.service.impl;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import javax.annotation.PostConstruct;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import at.a1ta.bite.core.server.dao.PersonDao;
import at.a1ta.bite.core.shared.BaseStrategyHolder;
import at.a1ta.bite.core.shared.Strategy;
import at.a1ta.bite.core.shared.StrategyHolder;
import at.a1ta.bite.core.shared.dto.cd.CdPerson;
import at.a1ta.bite.data.clarify.service.ClarifyInteractionService;
import at.a1ta.bite.data.clarify.shared.dto.ClarifyInteraction;
import at.a1ta.cuco.core.dao.db.PayableTicketDao;
import at.a1ta.cuco.core.dao.esb.BrianDao;
import at.a1ta.cuco.core.service.PayableTicketService;
import at.a1ta.cuco.core.shared.dto.Party;
import at.a1ta.cuco.core.shared.dto.PayableTicket;

@Service
public class PayableTicketServiceImpl implements PayableTicketService {
  private static final Logger logger = LoggerFactory.getLogger(PayableTicketServiceImpl.class);

  private PayableTicketDao payableTicketDao;
  private ClarifyInteractionService interactionService;

  private StrategyHolder<Strategy<PayableTicket>, PayableTicket> holder;

  private PersonDao personDao;

  private BrianDao brianDao;

  public PayableTicketServiceImpl() {

  }

  PayableTicketServiceImpl(List<Strategy<PayableTicket>> strategies) {
    this.holder = new PayableTicketStrategyHolder(strategies);
  }

  @Override
  public List<PayableTicket> getTicketsForParties(List<Party> parties) {
    return payableTicketDao.getTicketsForParties(parties);
  }

  @Override
  @Transactional(value = "transactionManager")
  public void insertTicket(PayableTicket ticket) {
    try {
      if (ticket.getService().getChargingType().getId().equals(3L)) {
        ticket.setExportedDate(new Date());
      }

      this.holder.handle(ticket);
      logger.info("PAST ticket for customer=" + ticket.getCustomerId() + ", onkz=" + ticket.getOnkz() + ", lknz=" + ticket.getLknz() + ", number=" + ticket.getNumber() + ", service id="
          + ticket.getService().getId() + " created.");
    } catch (Exception e) {
      logger.error("Error inserting PAST ticket", e);
      throw e;
    }
  }

  /**
   * Ticket strategy holder taking care of handling tickets
   */
  private static class PayableTicketStrategyHolder extends BaseStrategyHolder<Strategy<PayableTicket>, PayableTicket> {

    protected PayableTicketStrategyHolder(List<Strategy<PayableTicket>> list) {
      super(list);
    }

  }

  /**
   * Saves Payable ticket to database and creates interaction for non mobile ones.
   */
  private class GlobalTicketStrategy implements Strategy<PayableTicket> {

    private final PayableTicketDao ticketDao;

    protected GlobalTicketStrategy(PayableTicketDao ticketDao) {
      this.ticketDao = ticketDao;
    }

    @Override
    public Object handle(PayableTicket value) {
      handleTicket(value);
      return Boolean.TRUE;
    }

    private void handleTicket(PayableTicket ticket) {
      if (ticket.getService().getChargingType().getId().equals(1L)) {
        if (ticket.getOnkz() == null || ticket.getOnkz().equals("") || ticket.getNumber() == null || ticket.getNumber().equals("")) {
          throw new RuntimeException("Number is null or empty");
        }
      } else if (ticket.getService().getChargingType().getId().equals(2L)) {
        if (ticket.getClearingAccountNumber() == null) {
          throw new RuntimeException("Clearingaccount is null");
        }
      }
      ticketDao.insertTicket(ticket);
    }

    @Override
    public boolean canHandle(PayableTicket candidate) {
      return true;
    }

  }

  /**
   * Writes interactions for non mobile tickets to ClarifyFixed
   */
  private class InteractionWritingStrategy implements Strategy<PayableTicket> {

    private final ClarifyInteractionService interactionService;

    public InteractionWritingStrategy(ClarifyInteractionService interactionService) {
      super();
      this.interactionService = interactionService;
    }

    @Override
    public Object handle(PayableTicket ticket) {
      writeInteraction(ticket);
      return Boolean.TRUE;
    }

    @Override
    public boolean canHandle(PayableTicket candidate) {
      if (candidate.getService() != null && candidate.getService().getChargingType() != null) {
        return !candidate.getService().getChargingType().isMobileChargingType();
      }
      return false;
    }

    private void writeInteraction(PayableTicket ticket) {
      try {
        interactionService.saveInteraction(getInteractionForTicket(ticket));
      } catch (Exception e) {
        StringWriter stack = new StringWriter();
        e.printStackTrace(new PrintWriter(stack));
        logger.debug("Exception: " + stack.toString());
        logger.error("Interaction for PaST Ticket " + (ticket != null ? ticket.getId() : "") + " could not be created.", e);
      }
    }

    private ClarifyInteraction getInteractionForTicket(PayableTicket ticket) {
      CdPerson agent = personDao.getPerson(ticket.getAgent().getUsername());
      ClarifyInteraction interaction = new ClarifyInteraction(ClarifyInteraction.Type.CONTACT);

      interaction.setPartyId(ticket.getCustomerId());
      interaction.setAgentUuser(ticket.getAgent().getUsername());
      interaction.setPhoneNumber(ticket.getOnkz() + ticket.getNumber());
      interaction.setInsertedBy("PaST");
      interaction.setDirection(ClarifyInteraction.Direction.INBOUND);
      interaction.setType("PaST");

      if (ticket.getService().getProduct() != null) {
        interaction.setProduct(ticket.getService().getProduct());
      }
      if (ticket.getService().getReason1() != null) {
        interaction.setReason1(ticket.getService().getReason1());
      }
      if (ticket.getService().getReason2() != null) {
        interaction.setReason2(ticket.getService().getReason2());
      }
      interaction.setReason3("Nettobetrag: " + ticket.getCosts() + "€");
      if (ticket.getService().getResult() != null) {
        interaction.setResult(ticket.getService().getResult());
      }

      String notes = "Agent: " + agent.getCn() + " (" + agent.getUuser() + ")\n";
      notes = notes + "Telefonnummer: " + ticket.getOnkz() + "/" + ticket.getNumber() + "\n\n";
      notes = notes + "Zusatzinfos:\n" + ticket.getComment();
      interaction.setNote(notes);

      return interaction;
    }
  }

  /**
   * Save ticket to ADX billing system (used for mobile/convergent products)
   */
  private class ADXTicketStrategy implements Strategy<PayableTicket> {

    private BrianDao brainDao;

    protected ADXTicketStrategy(BrianDao brainDao) {
      this.brainDao = brainDao;
    }

    @Override
    public Boolean handle(PayableTicket value) {
      addCredit(value);
      return Boolean.TRUE;
    }

    private void addCredit(PayableTicket ticket) {
      brainDao.addCreditRecord(ticket);
    }

    @Override
    public boolean canHandle(PayableTicket candidate) {
      if (candidate == null) {
        return false;
      }

      return candidate.getService().getChargingType().getId().equals(3L);
    }

  }

  @Autowired
  public void setPayableTicketDao(PayableTicketDao payableTicketDao) {
    this.payableTicketDao = payableTicketDao;
  }

  @Autowired
  public void setInteractionService(ClarifyInteractionService interactionService) {
    this.interactionService = interactionService;
  }

  @Autowired
  public void setBrianDao(BrianDao brianDao) {
    this.brianDao = brianDao;
  }

  @Autowired
  public void setPersonDao(PersonDao personDao) {
    this.personDao = personDao;
  }

  @PostConstruct
  public void afterPropertiesSet() {
    List<Strategy<PayableTicket>> strategies = new ArrayList<Strategy<PayableTicket>>();
    strategies.add(new GlobalTicketStrategy(this.payableTicketDao));
    strategies.add(new ADXTicketStrategy(brianDao));
    strategies.add(new InteractionWritingStrategy(interactionService));
    this.holder = new PayableTicketStrategyHolder(strategies);
  }
}
