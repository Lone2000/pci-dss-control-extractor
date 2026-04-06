import csv
import os

OUTPUT = r"c:\Users\PC\Desktop\Control Outputs\PCI_Controls_Preview.csv"

DOMAIN_3 = "Requirement 3: Protect Stored Account Data"
DOMAIN_4 = "Requirement 4: Protect Cardholder Data with Strong Cryptography During Transmission Over Open, Public Networks"
DOMAIN_5 = "Requirement 5: Protect All Systems and Networks from Malicious Software"
DOMAIN_6 = "Requirement 6: Develop and Maintain Secure Systems and Software"

existing_count = 0
if os.path.exists(OUTPUT):
    with open(OUTPUT, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and row[0]:
                existing_count += 1

controls = [
    # ── Requirement 3 continued (pages 55-71) ──
    {
        "identifier": "3.5.1.2",
        "domain": DOMAIN_3,
        "description": "If disk-level or partition-level encryption (rather than file-, column-, or field-level database encryption) is used to render PAN unreadable, it is implemented only as follows: On removable electronic media; OR If used for non-removable electronic media, PAN is also rendered unreadable via another method that meets Requirement 3.5.1.",
        "guidance": "Disk-level and partition-level encryption typically encrypts the entire disk or partition using the same key, with all data decrypted when the system is running or when an authorized user requests it. For this reason, disk-level encryption is not appropriate to protect stored PAN on computers, laptops, servers, storage arrays, or any other system that provides transparent decryption upon user authentication. Where available, following vendor hardening and best practice guidelines can assist in securing PAN on these devices.",
    },
    {
        "identifier": "3.5.1.3",
        "domain": DOMAIN_3,
        "description": "If disk-level or partition-level encryption is used (rather than file-, column-, or field-level database encryption) to render PAN unreadable, it is managed independently as follows: Logical access is managed separately and independently of native operating system authentication and access control mechanisms; Decryption keys are not associated with user accounts; Authentication factors (passwords, passphrases, or cryptographic keys) that allow access to unencrypted data are stored securely.",
        "guidance": "Disk-level encryption typically encrypts the entire disk or partition using the same key, with all data decrypted when the system is running or when an authorized user requests it. Many disk-encryption solutions intercept operating system read/write operations and carry out the appropriate cryptographic transformations without any special action by the user other than supplying a password or passphrase upon system start-up or at the beginning of a session. This provides no protection from a malicious individual who has already gained access to a valid user account. Full disk encryption helps to protect data in the event of physical loss of a disk and therefore its use is best limited only to removable electronic media storage devices.",
    },
    {
        "identifier": "3.6.1",
        "domain": DOMAIN_3,
        "description": "Procedures are defined and implemented to protect cryptographic keys used to protect stored account data against disclosure and misuse that include: Access to keys is restricted to the fewest number of custodians necessary; Key-encrypting keys are at least as strong as the data-encrypting keys they protect; Key-encrypting keys are stored separately from data-encrypting keys; Keys are stored securely in the fewest possible locations and forms.",
        "guidance": "Cryptographic keys must be strongly protected because those who obtain access will be able to decrypt data. Having a centralized key management system based on industry standards is recommended for managing cryptographic keys.",
    },
    {
        "identifier": "3.6.1.1",
        "domain": DOMAIN_3,
        "description": "An inventory of the entity's trusted keys and certificates used to protect PAN during transmission is maintained.",
        "guidance": "Maintaining an inventory of trusted keys helps the entity keep track of the algorithms, protocols, key strength, key expiry dates, and HSM location for each key. Having such an inventory allows the entity to quickly identify and address any vulnerabilities discovered in encryption software. For certificates, the inventory should include the issuing CA and certification expiration date.",
    },
    {
        "identifier": "3.6.1.2",
        "domain": DOMAIN_3,
        "description": "Secret and private keys used to encrypt/decrypt stored account data are stored in one (or more) of the following forms at all times: Encrypted with a key-encrypting key that is at least as strong as the data-encrypting key, and that is stored separately from the data-encrypting key; Within a secure cryptographic device (SCD), such as a hardware security module (HSM) or PTS-approved point-of-interaction device; As at least two full-length key components or key shares, in accordance with an industry-accepted method.",
        "guidance": "Storing cryptographic keys securely prevents unauthorized or unnecessary access that could result in the exposure of stored account data. Storing keys separately means they are stored in such a way that if the location of one key is compromised, the second key is not also compromised. Where data-encrypting keys are stored in an HSM, the HSM interaction channel should be protected to prevent interception of encryption or decryption operations.",
    },
    {
        "identifier": "3.6.1.3",
        "domain": DOMAIN_3,
        "description": "Access to cleartext cryptographic key components is restricted to the fewest number of custodians necessary.",
        "guidance": "Restricting the number of people who have access to cleartext cryptographic key components reduces the risk of stored account data being retrieved or rendered visible by unauthorized parties. Only personnel with defined key custodian responsibilities (creating, altering, rotating, distributing, or otherwise maintaining encryption keys) should be granted access to key components.",
    },
    {
        "identifier": "3.6.1.4",
        "domain": DOMAIN_3,
        "description": "Cryptographic keys are stored in the fewest possible locations.",
        "guidance": "Storing cryptographic keys in the fewest locations helps an organization keep track and monitor all key locations and minimizes the potential for keys to be exposed to unauthorized parties.",
    },
    {
        "identifier": "3.7.1",
        "domain": DOMAIN_3,
        "description": "Key-management policies and procedures are implemented to include generation of strong cryptographic keys.",
        "guidance": "Using strong cryptographic keys significantly increases the level of security of encrypted account data.",
    },
    {
        "identifier": "3.7.2",
        "domain": DOMAIN_3,
        "description": "Key-management policies and procedures are implemented to include secure distribution of cryptographic keys.",
        "guidance": "Secure distribution or conveyance of secret or private cryptographic keys means that keys are distributed only to authorized custodians, as identified in Requirement 3.6.1.2, and are never distributed insecurely.",
    },
    {
        "identifier": "3.7.3",
        "domain": DOMAIN_3,
        "description": "Key-management policies and procedures are implemented to include secure storage of cryptographic keys.",
        "guidance": "Storing keys without proper protection could provide access to attackers, resulting in the decryption and exposure of account data. Secure storage of keys can be achieved by encrypting them with a key-encrypting key.",
    },
    {
        "identifier": "3.7.4",
        "domain": DOMAIN_3,
        "description": "Key-management policies and procedures are implemented for cryptographic key changes for keys that have reached the end of their cryptoperiod, as defined by the associated application vendor or key owner, and based on industry best practices and guidelines, including the following: A defined cryptoperiod for each key type in use; A process for key changes at the end of the defined cryptoperiod.",
        "guidance": "Retiring encryption keys when they reach the end of their cryptoperiod is imperative to minimize the risk of someone obtaining the encryption keys and using them to decrypt data. A cryptoperiod is the time span during which a cryptographic key can be used for its defined purpose. Considerations for defining the cryptoperiod include, but are not limited to, the strength of the underlying algorithm, size or length of the key, risk of key compromise, and the sensitivity of the data being encrypted.",
    },
    {
        "identifier": "3.7.5",
        "domain": DOMAIN_3,
        "description": "Key-management policies and procedures are implemented to include the retirement, replacement, or destruction of keys as deemed necessary when: The integrity of the key has been weakened, including but not limited to departure of an employee with knowledge of a cleartext key component; A key is suspected of or known to be compromised; The key component leaves the company, or the role for which the key component was known is no longer in use.",
        "guidance": "Keys that are no longer required, keys with weakened integrity, and keys that are known or suspected to be compromised, should be archived, revoked, and/or destroyed to ensure that the keys can no longer be used. If such keys need to be kept (for example, to support archived encrypted data), they should be strongly protected. The encryption solution should provide for and facilitate a key replacement process. If retired or replaced cryptographic keys need to be retained, these keys must be securely archived (for example, by using a key-encrypting key). Archived cryptographic keys should only be used for decryption/verification purposes.",
    },
    {
        "identifier": "3.7.6",
        "domain": DOMAIN_3,
        "description": "Where manual cleartext cryptographic key-management operations are used by personnel, key-management policies and procedures are implemented including managing these operations using split knowledge and dual control.",
        "guidance": "Split knowledge and dual control of keys are used to eliminate the possibility of a single person having access to the whole key and therefore being able to gain access to all the data. Split knowledge is a method in which two or more people separately have key components, where each person knows only their own key component, and the individual key components convey no knowledge of the whole cryptographic key. Dual control requires two or more people to perform an operation, and no single person can access or use the authentication factor of another. Where key components or key shares are used, procedures should ensure that no single custodian ever has access to sufficient key components to reconstruct the cryptographic key.",
    },
    {
        "identifier": "3.7.7",
        "domain": DOMAIN_3,
        "description": "Key-management policies and procedures are implemented to include the prevention of unauthorized substitution of cryptographic keys.",
        "guidance": "If an attacker is able to substitute an entity's key with a key the attacker knows, the attacker will be able to decrypt all data encrypted with that key. The encryption solution should not allow for or accept substitution of keys from unauthorized sources or unexpected processes. Controls should include ensuring that individuals with access to key components cannot substitute new key components and the encryption solution not accepting cryptographic keys from unauthorized sources or via any unauthorized processes.",
    },
    {
        "identifier": "3.7.8",
        "domain": DOMAIN_3,
        "description": "Key-management policies and procedures are implemented to include that key custodians formally acknowledge (in writing or electronically) that they understand and accept their key-custodian responsibilities.",
        "guidance": "This process will help ensure individuals that act as key custodians commit to the key-custodian role and understand and accept the responsibilities.",
    },
    {
        "identifier": "3.7.9",
        "domain": DOMAIN_3,
        "description": "Additional requirement for service providers: Where a service provider shares cryptographic keys with its customers for transmission or storage of account data, guidance on the secure transmission, storage, and update of such keys is documented and distributed to the service provider's customers.",
        "guidance": "Providing guidance to customers on how to securely transmit, store, and update cryptographic keys can help prevent keys from being mismanaged or disclosed to unauthorized entities.",
    },
    # ── Requirement 4 (pages 72-80) ──
    {
        "identifier": "4.1.1",
        "domain": DOMAIN_4,
        "description": "All security policies and operational procedures that are identified in Requirement 4 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 4.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 4. While it is important to define the specific policies or procedures called out in Requirement 4, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "4.1.2",
        "domain": DOMAIN_4,
        "description": "Roles and responsibilities for performing activities in Requirement 4 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "4.2.1",
        "domain": DOMAIN_4,
        "description": "Strong cryptography and security protocols are implemented as follows to safeguard PAN during transmission over open, public networks: Only trusted keys and certificates are accepted; Certificates used to safeguard PAN during transmission over open, public networks are confirmed as valid and are not expired or revoked; The protocol in use supports only secure versions or configurations and does not support fallback to, or use of insecure versions, algorithms, key sizes, or implementations; The encryption strength is appropriate for the encryption methodology in use.",
        "guidance": "Sensitive information must be encrypted during transmission over public networks because it is easy and common for a malicious individual to intercept and/or divert data while in transit. The network and data-flow diagrams defined in Requirement 1 are useful resources for identifying all connection points where account data is transmitted or received over open, public networks. PAN transmissions can be protected by encrypting the data before it is transmitted, or by encrypting the session over which the data is transmitted, or both. It is not required that strong cryptography be applied at both the data level and the session level, it is recommended that all transmissions be encrypted using strong cryptography.",
    },
    {
        "identifier": "4.2.1.1",
        "domain": DOMAIN_4,
        "description": "An inventory of the entity's trusted keys and certificates used to protect PAN during transmission is maintained.",
        "guidance": "Maintaining an inventory of trusted keys and certificates helps the entity keep track of the algorithms, protocols, key strength, key expiry dates, and key custodian for each key and certificate. For certificates, the inventory should include the issuing CA and certification expiration date.",
    },
    {
        "identifier": "4.2.1.2",
        "domain": DOMAIN_4,
        "description": "Wireless networks transmitting PAN or connected to the CDE use industry best practices to implement strong cryptography for authentication and transmission.",
        "guidance": "Since wireless networks do not require physical media to connect, it is important to establish controls limiting who can connect and what transmission protocols will be used. Malicious users use free and widely available tools to eavesdrop on wireless communications. Use of strong cryptography can help limit disclosure of sensitive information across wireless networks. Wireless networks should not be considered or used as a transport protocol or lower layer. A wireless network that does not meet the intent of strong cryptography should not be used to transmit PAN or connect to the CDE.",
    },
    {
        "identifier": "4.2.2",
        "domain": DOMAIN_4,
        "description": "PAN is secured with strong cryptography whenever it is sent via end-user messaging technologies.",
        "guidance": "End-user messaging technologies typically can be easily intercepted by packet-sniffing during delivery across internal and public networks. The use of end-user messaging technology to send PAN should only be considered where there is a defined and documented business need. PAN sent via end-user messaging technologies should be controlled through the Acceptable Use Policies defined by the entity.",
    },
    # ── Requirement 5 (pages 81-95) ──
    {
        "identifier": "5.1.1",
        "domain": DOMAIN_5,
        "description": "All security policies and operational procedures that are identified in Requirement 5 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 5.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 5. While it is important to define the specific policies or procedures called out in Requirement 5, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "5.1.2",
        "domain": DOMAIN_5,
        "description": "Roles and responsibilities for performing activities in Requirement 5 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "5.2.1",
        "domain": DOMAIN_5,
        "description": "An anti-malware solution(s) is deployed on all system components, except for those system components identified in periodic evaluations per Requirement 5.2.3 that concludes the system components are not at risk from malware.",
        "guidance": "There is a constant stream of attacks targeting newly discovered vulnerabilities in systems previously regarded as secure. Without an anti-malware solution that is updated regularly, new forms of malware can be used to attack the network, or to exploit vulnerabilities in systems, and compromise data. It is important to protect against all types and forms of malware to prevent malicious software from entering the network. Entities should also be aware of zero-day attacks (those that exploit a previously unknown vulnerability) and consider solutions and processes that monitor for unexpected behavior.",
    },
    {
        "identifier": "5.2.2",
        "domain": DOMAIN_5,
        "description": "The deployed anti-malware solution(s): Detects all known types of malware; Removes, blocks, or contains all known types of malware.",
        "guidance": "It is important to protect against all types and forms of malware to prevent unauthorized access. Anti-malware solutions may include a combination of network-based controls, host-based controls, and endpoint security solutions. In addition to signature-based tools, anti-malware solutions include sandboxing, privilege escalation controls, and machine learning.",
    },
    {
        "identifier": "5.2.3",
        "domain": DOMAIN_5,
        "description": "Any system components that are not at risk for malware are evaluated periodically to include the following: A documented list of all system components not at risk for malware; Identification and evaluation of evolving malware threats for those system components; Confirmation whether such system components continue to not require anti-malware protection.",
        "guidance": "Certain systems, at a given point in time, may not currently be commonly targeted or affected by malware. However, industry trends for malware can change quickly, so it is important for organizations to be aware of new malware that might affect their systems, for example, by monitoring vendor security notices and anti-malware forums to determine whether its systems might be coming under threat from new and evolving malware. Trends in malware should be included in the identification of new security vulnerabilities at Requirement 6.3.1, and methods to address new trends should be incorporated into the entity's configuration standards and protection mechanisms as needed. If an entity determines that a particular system is not susceptible to any type of malware, the entity should provide supporting documentation to provide justification, include hardening of the system to prevent malware, and reevaluate at least every 12 months.",
    },
    {
        "identifier": "5.2.3.1",
        "domain": DOMAIN_5,
        "description": "The frequency of periodic evaluations of system components identified as not at risk for malware is defined in the entity's targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1.",
        "guidance": "Entities determine the optimum period to undertake periodic evaluations based on criteria such as the complexity of each entity's environment and the number and types of systems that need to be evaluated.",
    },
    {
        "identifier": "5.3.1",
        "domain": DOMAIN_5,
        "description": "The anti-malware solution(s) is kept current via automatic updates.",
        "guidance": "For an anti-malware solution to remain effective, it needs to have the latest security updates, signatures, threat analysis engines, and any other updates that the anti-malware vendor identifies as being critical to maintaining the effectiveness of the solution. Keeping up to date with the latest updates and patches is important to address evolving and emerging threats. Anti-malware mechanisms should be updated as quickly as possible after an update is available, to ensure the most current protection against new and evolving threats. Updates may be automatically downloaded and distributed to end-user systems and may need to be automatically communicated to individual system components prior to being deployed.",
    },
    {
        "identifier": "5.3.2",
        "domain": DOMAIN_5,
        "description": "The anti-malware solution(s): Performs periodic scans and active or real-time scans; OR Performs continuous behavioral analysis of systems or processes.",
        "guidance": "Anti-malware solutions can identify malware that is present but not currently inactive within the environment. Some anti-malware solutions can identify malware not currently active, for example, it might be dormant. Anti-malware solutions and tools can also help protect against previously unknown threats. On-demand and ongoing analysis helps ensure and confirm that malware is unable to execute on a system. Combined with anti-malware tools that monitor for unexpected behavior, detection of malware can be made more efficient through the use of anti-malware scanning tools.",
    },
    {
        "identifier": "5.3.2.1",
        "domain": DOMAIN_5,
        "description": "If periodic malware scans are performed to meet Requirement 5.3.2, the frequency of scans is defined in the entity's targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1.",
        "guidance": "Entities can determine the optimum period to undertake periodic scans based on their own assessment of the risks posed to their environments.",
    },
    {
        "identifier": "5.3.3",
        "domain": DOMAIN_5,
        "description": "For removable electronic media, the anti-malware solution(s): Performs automatic scans of when the media is inserted, connected, or logically mounted; OR Performs continuous behavioral analysis of systems or processes when the media is inserted, connected, or logically mounted.",
        "guidance": "Portable media devices are often overlooked as an entry method for malware. Attackers will often pre-load malware onto portable devices such as USB and flash drives and leave them in public places, such as parking lots of companies known to be targets. An unsuspecting user then finds the device and inserts it into their computer, which then triggers the malware, introducing new threats within the environment.",
    },
    {
        "identifier": "5.3.4",
        "domain": DOMAIN_5,
        "description": "Audit logs for the anti-malware solution(s) are enabled and retained in accordance with Requirement 10.5.1.",
        "guidance": "It is important to track the effectiveness of the anti-malware mechanisms and controls—for example, by logging malware detections, corrective actions, generation of alerts, update failures, and whether anti-malware scans are being performed and completed. Anti-malware logs also allow an entity to determine how malware entered the environment and track its activity when inside the entity's network.",
    },
    {
        "identifier": "5.3.5",
        "domain": DOMAIN_5,
        "description": "Anti-malware mechanisms cannot be disabled or altered by users, unless specifically documented and authorized by management on a case-by-case basis for a limited time period.",
        "guidance": "It is important that defensive mechanisms are always running so that malware is detected in real time. Ad hoc disabling of anti-malware solutions can provide opportunities for malware to propagate and can result in system compromise. A system's anti-malware protection needs to be proactively maintained to support a system's continuous ability to detect and stop malware from being introduced, including on administrators' computers. Alerting when anti-malware is disabled will allow for timely management awareness and correction so that anti-malware protection is not inactive and malware can be blocked from entering the environment.",
    },
    {
        "identifier": "5.4.1",
        "domain": DOMAIN_5,
        "description": "Processes and automated mechanisms are in place to detect and protect personnel against phishing attacks.",
        "guidance": "Technical controls can limit the number of occasions personnel have to evaluate the veracity of a communication and can also limit the effects of individual responses to phishing. When developing anti-phishing controls, entities are encouraged to consider a combination of approaches, such as using anti-spoofing controls, DKIM (DomainKeys Identified Mail), Domain-based Message Authentication Reporting and Conformance (DMARC), SPF, and Domain Keys to help detect and prevent phishing. The deployment of technologies for blocking phishing e-mails and malware before they reach personnel, such as link scrubbers and server-side anti-malware, can reduce the number of incidents and can also assist in blocking attempts before they reach individual users. Additionally, training personnel to detect and report phishing attempts is also important.",
    },
    # ── Requirement 6 (pages 96-110) ──
    {
        "identifier": "6.1.1",
        "domain": DOMAIN_6,
        "description": "All security policies and operational procedures that are identified in Requirement 6 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 6.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 6. While it is important to define the specific policies or procedures called out in Requirement 6, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "6.1.2",
        "domain": DOMAIN_6,
        "description": "Roles and responsibilities for performing activities in Requirement 6 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "6.2.1",
        "domain": DOMAIN_6,
        "description": "Bespoke and custom software are developed securely, as follows: Based on industry standards and/or best practices for secure development; In accordance with PCI DSS (for example, secure authentication and logging); Incorporating consideration of information security issues during each stage of the software development lifecycle.",
        "guidance": "Without the inclusion of security during the requirements definition, design, analysis, and testing phases of software development, security vulnerabilities can be inadvertently or maliciously introduced into the production environment. Understanding how sensitive data is handled by the application—including when stored, transmitted, and in memory—can help identify where data needs to be protected. It is important to consider building security into software from the initial design stage rather than trying to retrofit the software later.",
    },
    {
        "identifier": "6.2.2",
        "domain": DOMAIN_6,
        "description": "Software development personnel working on bespoke and custom software are trained at least once every 12 months as follows: On software security relevant to their job function and development languages; Including secure software design and secure coding techniques.",
        "guidance": "Having staff knowledgeable in secure coding methods, including techniques defined in Requirement 6.2.4, will help minimize the number of security vulnerabilities introduced through poor coding practices. Training for developers may be provided in-house or by third parties. Training should include, but is not limited to, design, coding techniques/methodologies, frameworks, and tools. Secure coding training may need to be updated as industry-accepted secure coding practices change and as new threats emerge. As industry-accepted secure coding practices evolve, organizational coding practices and developer training may need to be updated to address new threats.",
    },
    {
        "identifier": "6.2.3",
        "domain": DOMAIN_6,
        "description": "Bespoke and custom software is reviewed prior to being released into production or to customers, to identify and correct potential coding vulnerabilities, as follows: Code reviews ensure code is developed in accordance with secure coding guidelines; Code reviews look for both existing and emerging software vulnerabilities; Appropriate corrections are implemented prior to release.",
        "guidance": "Security vulnerabilities in bespoke and custom software are commonly exploited by malicious individuals to gain access to a network and compromise account data. Vulnerabilities can be introduced in code at any point during the development process. Vulnerable code is far more difficult and expensive to address after it has been deployed or released into production environments. Including a formal review and corrections before release helps to confirm that code is authored in a manner that includes appropriate defensive coding techniques. Having a formal code review methodology and review process helps to improve the quality of the finished code.",
    },
    {
        "identifier": "6.2.3.1",
        "domain": DOMAIN_6,
        "description": "If manual code reviews are performed for bespoke and custom software prior to release to production, code changes are: Reviewed by individuals other than the originating code author, and who are knowledgeable about code-review techniques and secure coding practices; Reviewed and approved by management prior to release.",
        "guidance": "Code that is reviewed by someone other than the original author, who is both experienced in code reviews and knowledgeable about secure coding practices, minimizes the possibility that code containing security or logic errors that could affect the security of cardholder data is released into a production environment. Having a formal review methodology and review process helps to improve the quality of the finished code. Code review is a tiring process, and for this reason, it is important to ensure reviewers are not reviewing too much at a time.",
    },
    {
        "identifier": "6.2.4",
        "domain": DOMAIN_6,
        "description": "Software engineering techniques or other methods are defined and used by software development personnel to prevent or mitigate common software attacks and related vulnerabilities in bespoke and custom software, including but not limited to: Injection attacks, including SQL, LDAP, XPath, or other command, parameter, object, fault, or injection-type flaws; Attacks on data and data structures, including attempts to manipulate buffers, pointers, input data, or shared data; Attacks on cryptography usage, including attempts to exploit weak, insecure, or inappropriate cryptographic implementations, algorithms, cipher suites, or modes of operation; Attacks on business logic, including attempts to abuse or bypass application features and functionalities through the manipulation of APIs, communication protocols and channels, client-side functionality, or other system/application functions and resources; Attacks on access control mechanisms, including attempts to bypass or abuse identification, authentication, or authorization mechanisms, or attempts to exploit weaknesses in the implementation of such mechanisms; Attacks via any other input to the application or systems (XSS) and cross-site request forgery (CSRF).",
        "guidance": "Detecting or preventing common errors that result in vulnerable code as early as possible in the software development process lowers the probability that such errors make it through to production and lead to a compromise. Having formal engineering techniques and tools embedded in the development process will catch these errors early. For bespoke and custom software, the entity must ensure that code is developed focusing on the prevention or mitigation of common software attacks, including those described in this requirement.",
    },
    {
        "identifier": "6.3.1",
        "domain": DOMAIN_6,
        "description": "Security vulnerabilities are identified and managed as follows: New security vulnerabilities are identified using industry-recognized sources for security vulnerability information, including alerts from international and national computer emergency response teams (CERTs); Vulnerabilities are assigned a risk ranking based on industry best practices and consideration of potential impact; Risk rankings identify, at a minimum, all vulnerabilities considered to be a high-risk or critical to the environment; Vulnerabilities for bespoke and custom, and third-party software (for example, operating systems and databases) are covered.",
        "guidance": "Classifying the risks (for example, as critical, high, medium, or low) allows organizations to identify, prioritize, and address the highest risk items more quickly and reduce the likelihood that vulnerabilities posing the greatest risk will be exploited. Methods for evaluating vulnerabilities and assigning risk ratings will vary based on an organization's environment and risk-assessment strategy. When an entity is assigning its risk rankings, it should consider using a formal, objective, justifiable methodology that accurately portrays the risks of the vulnerabilities being prioritized. An organization is not expected to address all identified vulnerabilities. The entity should focus on the vulnerabilities that are most important and have the highest risk.",
    },
    {
        "identifier": "6.3.2",
        "domain": DOMAIN_6,
        "description": "An inventory of bespoke and custom software, and third-party software components incorporated into bespoke and custom software is maintained to facilitate vulnerability and patch management.",
        "guidance": "Identifying and listing all the entity's bespoke and custom software, and any third-party software that is incorporated into the entity's bespoke and custom software enables the entity to promptly identify and address vulnerabilities. Maintaining an inventory of these components allows the entity to address known vulnerabilities in the entity's software by identifying vulnerable components and proactively patching them. An entity's inventory should cover all payment software components and dependencies, including supported execution platforms or environments, third-party libraries, services, and other required components.",
    },
    {
        "identifier": "6.3.3",
        "domain": DOMAIN_6,
        "description": "All system components are protected from known vulnerabilities by installing applicable security patches/updates as follows: Patches/updates for critical vulnerabilities (identified according to the risk ranking process at Requirement 6.3.1) are installed within one month of release; All other applicable security patches/updates are installed within an appropriate time frame as determined by the entity's risk assessment (for example, within three months of release) and as identified by the entity's assessment of Requirement 6.3.1.",
        "guidance": "New exploits are constantly being discovered, and these can permit attacks against systems that have previously been considered secure. If the most recent patches/updates are not implemented on critical systems as soon as possible, a malicious individual can exploit these vulnerabilities to attack or disable a system or gain access to sensitive data. Prioritizing security patches/updates for critical infrastructure ensures that high-priority systems and devices are protected from vulnerabilities as soon as possible after a patch is released. An entity's patching cadence should factor in any re-evaluation of vulnerabilities and subsequent changes to the criticality of a vulnerability based on additional information. For example, a vulnerability initially identified as low risk could subsequently pose a higher risk, and a high-risk vulnerability could collectively pose a low or medium risk if it is present on the same system, or if additional compensating controls are applied.",
    },
]

with open(OUTPUT, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for i, c in enumerate(controls, start=existing_count + 1):
        writer.writerow([
            i, "", c["description"], "", c["domain"],
            7, c["identifier"], c["guidance"],
            "Yes", "", "", "",
        ])

print(f"Appended {len(controls)} controls (IDs {existing_count+1}-{existing_count+len(controls)})")
print(f"Total rows now: {existing_count + len(controls)}")
