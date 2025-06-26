package at.a1ta.cuco.core.dao.esb;

import java.rmi.RemoteException;
import java.util.ArrayList;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import at.a1ta.bite.core.server.esb.BaseEsbClient;
import at.a1ta.bite.core.server.esb.EsbException;
import at.a1ta.bite.core.server.service.SettingService;
import at.a1ta.cuco.core.shared.dto.PointOfSaleInfo;
import at.a1ta.cuco.core.shared.dto.StandardAddress;
import at.a1ta.cuco.core.shared.dto.StandardAddress.AddressDataSource;
import at.telekom.eai.kumscommon.xsd.Address;
import at.telekom.eai.kumscommon.xsd.GetPointOfSaleListRequestDocument;
import at.telekom.eai.kumscommon.xsd.GetPointOfSaleListResponse;
import at.telekom.eai.kumscommon.xsd.GetPointOfSaleListResponseDocument;
import at.telekom.eai.kumscommon.xsd.PointOfSaleList;
import at.telekom.eai.kumscommon.xsd.PointOfSaleType;

import com.telekomaustriagroup.esb.kumscommon.KUMSCommonStub;
import com.telekomaustriagroup.esb.kumscommon.KumsCommonFault;

@Repository
public class KUMSCommonDaoImpl extends BaseEsbClient<KUMSCommonStub> implements KUMSCommonDao {

  @Autowired
  private SettingService settingService;

  @Override
  public ArrayList<PointOfSaleInfo> loadAvailablePOSList() {

    GetPointOfSaleListRequestDocument requestDocument = createGetPointOfSaleListRequestDocument();

    ArrayList<PointOfSaleInfo> pointOfSalesList = new ArrayList<PointOfSaleInfo>();
    GetPointOfSaleListResponseDocument responseDocument;

    if (!settingService.getBooleanValue("testModeActive", false)) {

      try {
        responseDocument = stub.getPointOfSaleList(requestDocument, null);
        GetPointOfSaleListResponse response = responseDocument.getGetPointOfSaleListResponse();
        PointOfSaleList list = response.getPointOfSaleList();

        if (list != null) {
          for (PointOfSaleType p : list.getPointOfSaleArray()) {
            if (p != null) {
              PointOfSaleInfo info = new PointOfSaleInfo(PointOfSaleInfo.LOADED, p.getDealerNumber(), p.getName());
              info.setAddress(extractAddress(p.getAddress()));
              info.setDealerId(p.getDealerNumber());
              info.setDelearEmailId(p.getEmailAddress());
              info.setDealerName(p.getName());
              pointOfSalesList.add(info);
            }
          }
        }

      } catch (RemoteException e) {
        throw new EsbException(e);
      } catch (KumsCommonFault e) {
        throw new EsbException(e);
      }

    } else {
      PointOfSaleInfo info = new PointOfSaleInfo();

      info.setStaus(PointOfSaleInfo.LOADED);
      info.setDealerId("Mocked:");
      info.setDealerName("Mocked: Testhändler 1");
      info.setAddress(mockStandardAddress());
      pointOfSalesList.add(info);

      PointOfSaleInfo info2 = new PointOfSaleInfo();

      info2.setStaus(PointOfSaleInfo.LOADED);
      info2.setDealerId("Mocked:");
      info2.setDealerName("Mocked: Testhändler 2");
      info2.setAddress(mockStandardAddress());

      pointOfSalesList.add(info2);

      PointOfSaleInfo info3 = new PointOfSaleInfo();

      info3.setStaus(PointOfSaleInfo.LOADED);
      info3.setDealerId("Mocked:");
      info3.setDealerName("Mocked: Testhändler 3");
      info3.setAddress(mockStandardAddress());

      pointOfSalesList.add(info3);

    }

    return pointOfSalesList;
  }

  private GetPointOfSaleListRequestDocument createGetPointOfSaleListRequestDocument() {
    GetPointOfSaleListRequestDocument newInstance = GetPointOfSaleListRequestDocument.Factory.newInstance();
    newInstance.addNewGetPointOfSaleListRequest();
    return newInstance;
  }

  private StandardAddress extractAddress(Address kumsAddress) {
    StandardAddress address = new StandardAddress();
    if (kumsAddress != null) {
      address.setLkmsId(kumsAddress.getLkmsId());
      address.setStreet(kumsAddress.getStreet());
      address.setHouseNumber(kumsAddress.getHouseNumber());
      address.setBlock(kumsAddress.getBlock());
      address.setStaircase(kumsAddress.getStaircase());
      address.setFloorNumber(kumsAddress.getFloorNumber());
      address.setDoorNumber(kumsAddress.getDoorNumber());
      address.setAdditional(kumsAddress.getAdditional());
      address.setPostcode(kumsAddress.getPostcode());
      address.setCity(kumsAddress.getCity());
      address.setVillage(kumsAddress.getVillage());
      address.setCountry(kumsAddress.getCountry());
    }
    address.setDataSource(AddressDataSource.KUMS_COMMON_SERVICE);
    return address;
  }

  private StandardAddress mockStandardAddress() {
    StandardAddress address = new StandardAddress();
    address.setLkmsId("1212");
    address.setStreet("Schuttelstrasse");
    address.setHouseNumber("23-25A");
    address.setBlock("25");
    address.setStaircase("0");
    address.setFloorNumber("100");
    address.setDoorNumber("1011");
    address.setAdditional("");
    address.setPostcode("1020");
    address.setCity("Wien");
    address.setVillage("Wien");
    address.setCountry("Austria");
    address.setDataSource(AddressDataSource.PARTY_SERVICE);
    return address;
  }

}
