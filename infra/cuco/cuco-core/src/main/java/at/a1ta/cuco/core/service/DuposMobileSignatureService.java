package at.a1ta.cuco.core.service;

public interface DuposMobileSignatureService {

  String sendContractToSign(String jobId, byte[] data);
}
