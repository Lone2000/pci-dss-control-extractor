import csv
import os

OUTPUT = r"c:\Users\PC\Desktop\Control Outputs\PCI_Controls_Preview.csv"

DOMAIN_1 = "Requirement 1: Install and Maintain Network Security Controls"
DOMAIN_2 = "Requirement 2: Apply Secure Configurations to All System Components"
DOMAIN_3 = "Requirement 3: Protect Stored Account Data"

# Read existing rows to get the next Control ID
existing_count = 0
if os.path.exists(OUTPUT):
    with open(OUTPUT, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if row and row[0]:
                existing_count += 1

controls = [
    # ── Requirement 1 continued (pages 15-22) ──
    {
        "identifier": "1.3.3",
        "domain": DOMAIN_1,
        "description": "NSCs are installed between all wireless networks and the CDE, such that: All wireless traffic from wireless networks into the CDE is denied by default; Only wireless traffic with an authorized business purpose is allowed into the CDE.",
        "guidance": "Whether or not wireless technology is currently being used, or the entity has no plans to implement wireless technology, exploitation of wireless technology is a common path for malicious individuals to gain access to the network and account data. If a wireless network or device is installed without the entity's knowledge, it could easily allow a malicious individual to enter the network. If NSCs do not restrict access from wireless networks into the CDE, malicious individuals that gain unauthorized access to the wireless network can easily connect to the CDE and compromise account information.",
    },
    {
        "identifier": "1.4.1",
        "domain": DOMAIN_1,
        "description": "NSCs are implemented between trusted and untrusted networks.",
        "guidance": "Implementing NSCs at every connection coming to and from trusted and/or untrusted networks reduces the risk of a malicious individual gaining access to the entity's internal network and minimizes the chances of unauthorized connections. An example of a technology that manages connections between an untrusted network (for example, the Internet) and a trusted network is a DMZ, but that is separate from the entity's internal network and sometimes referred to as a perimeter network. Implementing NSCs at every connection protects the rest of the network in the event a single network or host becomes compromised.",
    },
    {
        "identifier": "1.4.2",
        "domain": DOMAIN_1,
        "description": "Inbound traffic from untrusted networks to trusted networks is restricted to: Communications with system components that are authorized to provide publicly accessible services, protocols, and ports; Stateful responses to communications initiated by system components in a trusted network; All other traffic is denied.",
        "guidance": "A system component that provides publicly accessible services to the outside (for example, email, web, DNS) is one that is at high risk for compromise. Separating such a system component into its own network segment, referred to as a DMZ, limits the exposure of the entity's internal network. System components that provide publicly accessible services and that need to be directly connected to the Internet are also sometimes referred to as bastion hosts. Where this functionality is provided as a built-in feature of the NSC, it should be verified that the functionality is active and properly configured. Having NSCs that deny all inbound traffic except specifically authorized connections reduces the risk of attacks from untrusted networks entering the entity's network.",
    },
    {
        "identifier": "1.4.3",
        "domain": DOMAIN_1,
        "description": "Anti-spoofing measures are implemented to detect and block forged source IP addresses from entering the trusted network.",
        "guidance": "Normally a packet contains the IP address of the computer that originally sent it so other computers in the network know where the packet came from. Malicious individuals will often try to spoof (or imitate) the sending IP address so that the target system believes the packet is from a trusted source. Filtering packets coming into the trusted network helps to, among other things, ensure packets are not spoofed to appear as if they are coming from the entity's own internal network. Products usually come with anti-spoofing set as a default and may not be configurable; entities should consult the vendor's documentation for more information.",
    },
    {
        "identifier": "1.4.4",
        "domain": DOMAIN_1,
        "description": "System components that store cardholder data are not directly accessible from untrusted networks.",
        "guidance": "Cardholder data that is directly accessible from an untrusted network, for example because it is stored on a system within a publicly accessible DMZ or in a cloud environment, is easier for an external attacker to access because there are fewer defensive layers to penetrate. Using NSCs to ensure that system components that store cardholder data are only directly accessed from trusted networks can prevent unauthorized network traffic from reaching the system component.",
    },
    {
        "identifier": "1.4.5",
        "domain": DOMAIN_1,
        "description": "The disclosure of internal IP addresses and routing information is limited to only authorized parties.",
        "guidance": "Restricting the disclosure of internal, private, and local IP addresses is useful to prevent a hacker from obtaining knowledge of these IP addresses and using that knowledge to access the network. Methods used to meet the intent of this requirement may vary depending on the specific networking technology being used. For example, the controls used to meet this requirement may be different for IPv4 networks than for IPv6 networks. Methods to obscure IP addressing may include but are not limited to: Network Address Translation (NAT), placing servers behind proxy servers, removal or filtering of route advertisements for internal networks that use registered addressing, and internal use of RFC 1918 (IPv4) or use IPv6 privacy extension (RFC 4941) when initiating outgoing sessions to the Internet.",
    },
    {
        "identifier": "1.5.1",
        "domain": DOMAIN_1,
        "description": "Security controls are implemented on any computing devices, including company- and employee-owned devices, that connect to both untrusted networks (including the Internet) and the CDE as follows: Specific configuration settings are defined to prevent threats being introduced into the entity's network; Security controls are actively running; Security controls are not alterable by users of the computing devices unless specifically documented and authorized by management on a case-by-case basis for a limited period.",
        "guidance": "Computing devices that are allowed to connect to the Internet from outside the corporate environment, for example, desktops, laptops, tablets, smartphones, and other mobile computing devices used by employees, are more vulnerable to Internet-based threats. Use of security controls such as host-based firewalls, endpoint protection solutions, and network-based security controls helps to protect devices from Internet-based attacks, which could use the device to gain access to the organization's systems and data when the device reconnects to the network. The specific configuration settings are determined by the entity and should be consistent with its network security policies. Practices include forbidding split tunneling of VPN connections for employee-owned or employee-managed devices and requiring that such devices boot up into a VPN.",
    },
    # ── Requirement 2 (pages 24-35) ──
    {
        "identifier": "2.1.1",
        "domain": DOMAIN_2,
        "description": "All security policies and operational procedures that are identified in Requirement 2 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 2.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 2. While it is important to define the specific policies or procedures called out in Requirement 2, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "2.1.2",
        "domain": DOMAIN_2,
        "description": "Roles and responsibilities for performing activities in Requirement 2 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "2.2.1",
        "domain": DOMAIN_2,
        "description": "Configuration standards are developed, implemented, and maintained to: Cover all system components; Address all known security vulnerabilities; Be consistent with industry-accepted system hardening standards or vendor hardening recommendations; Be updated as new vulnerability issues are identified, as defined in Requirement 6.3.1; Be applied when new systems are configured and verified as in place before or immediately after a system component is connected to a production environment.",
        "guidance": "There are known weaknesses with many operating systems, databases, network devices, software applications, container images, and other devices used within an entity's environment. There are also known ways to configure these system components to fix security vulnerabilities. Fixing security vulnerabilities reduces the opportunities available to an attacker. The specific controls to be applied to a system will be determined according to the function of the system. Numerous security organizations have established system-hardening guidelines and recommendations, which advise how to correct common weaknesses.",
    },
    {
        "identifier": "2.2.2",
        "domain": DOMAIN_2,
        "description": "Vendor default accounts are managed as follows: If the vendor default account(s) will be used, the default password is changed per Requirement 8.3.6; If the vendor default account(s) will not be used, the account is removed or disabled.",
        "guidance": "Malicious individuals often use vendor default account names and passwords to compromise operating systems, applications, and the systems on which they are installed. Because these default settings are often published and are well known, changing these settings will make systems less vulnerable to attack. Even if a default account is not intended to be used, changing the default password to a unique secure password and then disabling the account will prevent a malicious individual from re-enabling the account and gaining access with the default password. Entities should consider encrypting SAD with a different cryptographic key than the one used to encrypt PAN (note that if track data is part of track data) would need to be separately encrypted.",
    },
    {
        "identifier": "2.2.3",
        "domain": DOMAIN_2,
        "description": "Primary functions requiring different security levels are managed as follows: Only one primary function exists on a system component, OR Primary functions with differing security levels that exist on the same system component are isolated from each other, OR Primary functions with differing security levels on the same system component are all secured to the level required by the function with the highest security need.",
        "guidance": "Systems that combine a combination of services, protocols, and daemons for their primary function will have a security profile appropriate to allow that function to operate effectively. For example, systems that need to be directly connected to the Internet will have a particular security profile, like a DNS server, web server, or an e-commerce server. Conversely, other system components may operate a primary function comprising a different set of services, protocols, and daemons that performs functions that an entity does not want directly connected to the Internet. This requirement aims to ensure that different functions do not impact the security of other functions on the same server. Ideally, each function should be placed on different system components. This can be achieved with physical or virtual system components.",
    },
    {
        "identifier": "2.2.4",
        "domain": DOMAIN_2,
        "description": "Only necessary services, protocols, daemons, and functions are enabled, and all unnecessary functionality is removed or disabled.",
        "guidance": "Unnecessary services and functions can provide additional opportunities for malicious individuals to gain access to a system. By removing or disabling all unnecessary services, protocols, daemons, and functions, organizations can focus security measures on the functions that are necessary, reducing the risk that unknown or unnecessary functions will be exploited. Services and protocols that could be enabled by default but are commonly used by malicious individuals to compromise a system include, but are not limited to, removing all unnecessary functionality, scripts, drivers, features, subsystems, file systems, interfaces (USB and Bluetooth), and unnecessary web servers.",
    },
    {
        "identifier": "2.2.5",
        "domain": DOMAIN_2,
        "description": "If any insecure services, protocols, or daemons are present: Business justification is documented; Additional security features are documented and implemented that reduce the risk of using insecure services, protocols, or daemons.",
        "guidance": "Ensuring that all insecure services, protocols, and daemons are adequately secured with appropriate security features makes it more difficult for malicious individuals to exploit common points of compromise within a network. Insecure services, protocols, or daemons are deployed and their security features are configured into the configuration standards. This prevents insecure configurations from being introduced into the environment and provides additional security functions to assist with detection.",
    },
    {
        "identifier": "2.2.6",
        "domain": DOMAIN_2,
        "description": "System security parameters are configured to prevent misuse.",
        "guidance": "Correctly configuring security parameters provided in system components takes advantage of the capabilities of the system component to defeat malicious attacks. System configuration standards and related processes should specifically address security settings and parameters that have known security implications for each type of system component. Considerations should also include common security parameter settings for each type of system. In order for systems to be configured in accordance with the configuration standards, it is important that the standards are the basis for how systems are configured and that responsible personnel understand and follow the standards.",
    },
    {
        "identifier": "2.2.7",
        "domain": DOMAIN_2,
        "description": "All non-console administrative access is encrypted using strong cryptography.",
        "guidance": "If non-console administrative access uses unencrypted communications, an attacker can intercept the data, including administrative credentials such as IDs and passwords, to obtain the data and to use encrypted communications. Cleartext protocols (such as HTTP, telnet, etc.) do not encrypt traffic or logon details, making it easy for an eavesdropper to intercept this information. Non-console access may be facilitated by technologies that provide alternative access to systems, including but not limited to out-of-band (OOB), lights-out management (LOM), Intelligent Platform Management Interface (IPMI), and keyboard, video, mouse (KVM) switches with remote capabilities. These and other non-console access methods and technologies must be secured with strong cryptography. Refer to industry standards and best practices such as NIST SP 800-52 and SP 800-57.",
    },
    {
        "identifier": "2.3.1",
        "domain": DOMAIN_2,
        "description": "For wireless environments connected to the CDE or transmitting account data, all wireless vendor defaults are changed at installation or are confirmed to be secure, including but not limited to: Default wireless encryption keys; Passwords on wireless access points; SNMP defaults; Any other security-related wireless vendor defaults.",
        "guidance": "If wireless networks are not implemented with sufficient security configurations (including changing default settings), wireless sniffers can eavesdrop on the traffic, easily capture data and passwords, and easily enter and attack the network. In addition, key-management for wireless encryption should follow industry best practices as keys may easily be compromised. Wireless passwords should be constructed so that they are resistant to offline brute force attacks.",
    },
    {
        "identifier": "2.3.2",
        "domain": DOMAIN_2,
        "description": "For wireless environments connected to the CDE or transmitting account data, wireless encryption keys are changed as follows: Whenever personnel with knowledge of the key leave the company or the role for which the knowledge was necessary; Whenever a key is suspected of or known to be compromised.",
        "guidance": "Changing wireless encryption keys whenever someone with knowledge of the key leaves the organization or moves to a role that no longer requires knowledge of the key helps keep knowledge of keys limited to only those with a current business need to know. Also changing wireless encryption keys whenever a key is suspected or known to be compromised helps to minimize the risk of using those compromised keys to decrypt wireless traffic. This goal can be accomplished in multiple ways, including but not limited to generating and distributing new keys, using pre-shared keys, or via a defined points-of-authentication system (LAN). In addition, any keys that are known to be, or suspected of being, compromised should be managed in accordance with the entity's incident response plan at Requirement 12.10.1.",
    },
    # ── Requirement 3 (pages 37-54) ──
    {
        "identifier": "3.1.1",
        "domain": DOMAIN_3,
        "description": "All security policies and operational procedures that are identified in Requirement 3 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 3.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 3. While it is important to define the specific policies or procedures called out in Requirement 3, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "3.1.2",
        "domain": DOMAIN_3,
        "description": "Roles and responsibilities for performing activities in Requirement 3 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "3.2.1",
        "domain": DOMAIN_3,
        "description": "Account data storage is kept to a minimum through implementation of data retention and disposal policies, procedures, and processes that include at least the following: Coverage for all locations of stored account data; Coverage for any sensitive authentication data (SAD) stored prior to completion of authorization; Limiting data storage amount and retention time to that which is required for legal, regulatory, and/or business requirements; Specific retention requirements for stored account data that defines length of retention period and includes a documented business justification; Processes for secure deletion or rendering account data unrecoverable when no longer needed per the retention policy; A process for verifying, at least once every three months, that stored account data exceeding the defined retention period has been securely deleted or rendered unrecoverable.",
        "guidance": "A formal data retention policy identifies what data needs to be retained, for how long, and where that data resides so it can be securely destroyed or deleted as soon as it is no longer needed. The storage of SAD data prior to the completion of the authorization process is also addressed. The only account data that can be stored after authorization is the primary account number or PAN (rendered unreadable), expiration date, cardholder name, and service code. The storage of SAD data prior to the completion of the authorization is also addressed. When identifying locations of stored account data, consider all processes and personnel that access the data, as data could have been moved and stored in different locations than originally defined, including but not limited to backup and archive systems, removable data stores, paper-based media, and audio recordings.",
    },
    {
        "identifier": "3.3.1",
        "domain": DOMAIN_3,
        "description": "SAD is not stored after authorization, even if encrypted. All sensitive authentication data received is rendered unrecoverable upon completion of the authorization process.",
        "guidance": "SAD is very valuable to malicious individuals as it allows them to generate counterfeit payment cards and create fraudulent transactions. Therefore, the storage of SAD upon completion of the authorization process is prohibited. Entities that issue payment cards or that perform or support issuing services will often create and control sensitive authentication data as part of the issuing function. It is permissible for companies that issue payment cards or that perform, facilitate, or support issuing services to store sensitive authentication data only if there is a legitimate business need to store such data. SAD is only very sensitive data. Controls are in place to ensure that memory maintains a non-persistent state. It is not permissible to store SAD in persistent memory.",
    },
    {
        "identifier": "3.3.1.1",
        "domain": DOMAIN_3,
        "description": "The full contents of any track from the magnetic stripe on the back of a card, equivalent data contained on a chip, or elsewhere are not stored upon completion of the authorization process.",
        "guidance": "If full contents of any track (from the magnetic stripe on the back of a card, equivalent data contained on a chip, or elsewhere) is stored, malicious individuals who obtain that data can use it to reproduce payment cards and complete fraudulent transactions. Full track data is alternatively called full track, track, track 1, track 2, and magnetic-stripe data. Each track contains data elements that are specific to either the magnetic stripe or the chip and that may be treated differently. Data sources to review to ensure the full contents of any track are not retained upon completion of the authorization process include but are not limited to: incoming transaction data, all logs (for example, transaction, history, debugging, error), history files, trace files, database schemas, contents of databases, and on-premises and cloud data stores, any existing memory/crash dump files.",
    },
    {
        "identifier": "3.3.1.2",
        "domain": DOMAIN_3,
        "description": "The card verification code or value is not stored upon completion of the authorization process.",
        "guidance": "If card verification code or value data is stolen, malicious individuals can execute fraudulent Internet and mail-order/telephone-order (MO/TO) transactions. Securely deleting this data reduces the probability of it being compromised. If card verification codes are stored on paper media (for example, the card verification code or value written down during a card-not-present transaction), a method of securely destroying the paper media should be used. Data sources to review to ensure that the card verification code is not retained upon completion of the authorization process include, but are not limited to: incoming transaction data, all logs (for example, transaction, history, debugging, error), history files, trace files, database schemas, contents of databases, and on-premises and cloud data stores, any existing memory/crash dump files.",
    },
    {
        "identifier": "3.3.1.3",
        "domain": DOMAIN_3,
        "description": "The personal identification number (PIN) and the PIN block are not stored upon completion of the authorization process.",
        "guidance": "PIN and PIN blocks should be known only to the card owner or entity that issued the card. If this data is stolen, malicious individuals can execute PIN-based debit transactions (for example, in-store purchases and ATM withdrawals). Securely deleting this data reduces the probability of it being compromised. Data sources to review to ensure that PIN and PIN blocks are not retained upon completion of the authorization process include, but are not limited to: incoming transaction data, all logs (for example, transaction, history, debugging, error), history files, trace files, database schemas, contents of databases, and on-premises and cloud data stores, any existing memory/crash dump files.",
    },
    {
        "identifier": "3.3.2",
        "domain": DOMAIN_3,
        "description": "SAD that is stored electronically prior to completion of authorization is encrypted using strong cryptography.",
        "guidance": "SAD can be used by malicious individuals to increase the probability of successfully generating counterfeit payment cards and creating fraudulent transactions. Entities should consider encrypting SAD with a different cryptographic key than the one used to encrypt PAN. Note that this does not mean that PAN present in SAD (as part of track data) would need to be separately encrypted.",
    },
    {
        "identifier": "3.3.3",
        "domain": DOMAIN_3,
        "description": "Additional requirement for issuers and companies that support issuing services and store sensitive authentication data: Any storage of sensitive authentication data is: Limited to that which is needed for a legitimate issuing business need and is secured; Encrypted using strong cryptography.",
        "guidance": "SAD can be used by malicious individuals to increase the probability of successfully generating counterfeit payment cards and creating fraudulent transactions. Entities should consider encrypting SAD with a different cryptographic key than the one used to encrypt PAN. Note that this does not mean that PAN present in SAD (as part of track data) would need to be separately encrypted.",
    },
    {
        "identifier": "3.4.1",
        "domain": DOMAIN_3,
        "description": "PAN is masked when displayed (the BIN and last four digits are the maximum number of digits to be displayed), such that only personnel with a legitimate business need can see more than the BIN and last four digits of the PAN.",
        "guidance": "Use of full PAN on computer screens, payment card receipts, paper reports, etc. can result in this data being obtained by unauthorized individuals and used fraudulently. Displaying full PAN only for those with a legitimate business need minimizes the risk of unauthorized persons gaining access to PAN data. Applying access controls according to defined roles is one way to limit access. The masking approach should always display only the number of digits needed to perform a specific business function. For example, if only the last four digits are needed to perform a business function, mask the PAN so that individuals performing that function can view only the last four digits. As another example, if a function needs to view to the full PAN, the full PAN can be displayed for that function.",
    },
    {
        "identifier": "3.4.2",
        "domain": DOMAIN_3,
        "description": "When using remote-access technologies, technical controls prevent copy and/or relocation of PAN for all personnel, except for those with documented, explicit authorization and a legitimate, defined business need.",
        "guidance": "Relocation of PAN to unauthorized storage devices is a common way for this data to be obtained and used fraudulently. Methods to ensure that only those with explicit authorization and a legitimate business reason can copy or relocate PAN minimize the risk of unauthorized persons gaining access. Storing and/or copying of PAN onto local hard drives, removable electronic media, and other storage devices that are not permissible and not authorized for that individual is considered a violation of this requirement.",
    },
    {
        "identifier": "3.5.1",
        "domain": DOMAIN_3,
        "description": "PAN is rendered unreadable anywhere it is stored by using any of the following approaches: One-way hashes based on strong cryptography of the entire PAN; Truncation (hashing cannot be used to replace the truncated segment of PAN); If hashed and truncated versions of the same PAN, or different truncation formats of the same PAN, are present in an environment, additional controls are in place such that the different versions cannot be correlated to reconstruct the original PAN; Index tokens; Strong cryptography with associated key-management processes and procedures.",
        "guidance": "Rendering stored PAN unreadable is a defense-in-depth control designed to protect the data if an unauthorized individual gains access to stored data by exploiting a vulnerability or misconfiguration of an entity's primary access control. Secondary independent control systems provide extra security. A key is an essential element of strong cryptography. If an entity's primary access control fails, an attacker would only gain access to encrypted and unreadable PANs. It is a recognized technique used by industry for rendering data at rest unreadable. Strong cryptographic keys provide additional protection for data at rest.",
    },
    {
        "identifier": "3.5.1.1",
        "domain": DOMAIN_3,
        "description": "Hashes used to render PAN unreadable (per the first bullet of Requirement 3.5.1) are keyed cryptographic hashes of the entire PAN, with associated key-management processes and procedures in accordance with Requirements 3.6 and 3.7.",
        "guidance": "Rendering stored PAN unreadable is a defense-in-depth control designed to protect the data at an additional layer by implementing strong cryptographic controls, taking advantage of a vulnerability or misconfiguration of an entity's primary access control. A keyed cryptographic hash provides additional protection for the data at rest and additional resources. A system on which the hashes reside that stores account data also needs to be secured. Entities may consider implementing private-grain transit limitations between the hashes and the private key to more reliably implement processes and procedures at Requirement 3.6 and 3.7.",
    },
]

# Append to CSV
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
