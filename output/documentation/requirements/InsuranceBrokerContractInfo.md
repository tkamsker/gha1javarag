# Requirements Analysis: cuco-core/src/main/java/at/a1ta/cuco/core/shared/dto/InsuranceBrokerContractInfo.java

InsuranceBrokerContractInfo.java
1. Purpose and functionality:
- DTO for insurance broker contract information
- Stores device and contract-related details
- Supports GWT (Google Web Toolkit) parsing

2. User interactions:
- No direct user interactions - used as a data container

3. Data handling:
- Stores marketing contract type name
- Stores device marketing name
- Stores IMEI number
- Implements Serializable with version control

4. Business rules:
- Requires serialVersionUID for version control
- Default constructor required for GWT parsing

5. Dependencies:
- java.io.Serializable
- GWT framework compatibility
- Likely part of insurance/device management system