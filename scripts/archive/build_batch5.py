import csv
import os

OUTPUT = r"c:\Users\PC\Desktop\Control Outputs\PCI_Controls_Preview.csv"

DOMAIN_8 = "Requirement 8: Identify Users and Authenticate Access to System Components"
DOMAIN_9 = "Requirement 9: Restrict Physical Access to Cardholder Data"
DOMAIN_10 = "Requirement 10: Log and Monitor All Access to System Components and Cardholder Data"

existing_count = 0
if os.path.exists(OUTPUT):
    with open(OUTPUT, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and row[0]:
                existing_count += 1

controls = [
    # ── Requirement 8 continued (pages 159-171) ──
    {
        "identifier": "8.3.11",
        "domain": DOMAIN_8,
        "description": "Where authentication factors such as physical or digital security tokens, smart cards, or certificates are used: Factors are assigned to an individual user and not shared among multiple users; Physical and/or logical controls ensure only the intended user can use that factor to gain access.",
        "guidance": "If multiple users can use authentication factors such as tokens, smart cards, and certificates, it may be impossible to identify the individual using the authentication factor. Having physical and/or logical controls (for example, a PIN, biometric data, or a password) to uniquely authenticate the user of the account will prevent unauthorized users of the account from gaining access using a shared authentication factor.",
    },
    {
        "identifier": "8.4.1",
        "domain": DOMAIN_8,
        "description": "MFA is implemented for all non-console access into the CDE for personnel with administrative access.",
        "guidance": "Requiring more than one type of authentication factor reduces the probability that an attacker can gain access to a system by masquerading as a legitimate user, because the attacker would need to compromise multiple authentication factors. This is especially true in environments where traditionally the single authentication factor employed was something a user knows, such as a password or passphrase. Implementing MFA for non-console administrative access to in-scope system components that are part of or connected to the CDE prevents an administrator from using a single login factor to gain access to critical systems, and compromising in-scope system components.",
    },
    {
        "identifier": "8.4.2",
        "domain": DOMAIN_8,
        "description": "MFA is implemented for all access into the CDE.",
        "guidance": "Requiring more than one type of authentication factor reduces the probability that an attacker can gain access to a system by masquerading as a legitimate user, because the attacker would need to compromise multiple authentication factors. Implementing MFA for all access into the CDE adds an additional layer of protection for all connections to the CDE.",
    },
    {
        "identifier": "8.4.3",
        "domain": DOMAIN_8,
        "description": "MFA is implemented for all remote network access originating from outside the entity's network that could access or impact the CDE.",
        "guidance": "Requiring more than one type of authentication factor reduces the probability that an attacker can gain access to a system by masquerading as a legitimate user, because the attacker would need to compromise multiple authentication factors. Implementing MFA for all remote access originating from outside the entity's network provides an additional layer of security against unauthorized remote access.",
    },
    {
        "identifier": "8.5.1",
        "domain": DOMAIN_8,
        "description": "MFA systems are implemented as follows: The MFA system is not susceptible to replay attacks; MFA systems cannot be bypassed by any users, including administrative users, unless specifically documented and authorized by management on an exception basis, for a limited time period; At least two different types of authentication factors are used; Success of all authentication factors is required before access is granted.",
        "guidance": "Poorly configured MFA systems can be bypassed by attackers. If the MFA system is not configured to enforce all factors, it is possible that one factor may provide sufficient access. If the MFA system allows bypass, then a single authentication factor provides a single point of failure if compromised. Therefore, in these implementations, controls are needed to prevent unauthorized use of the MFA bypass. Using one type of factor twice (for example, using two separate passwords) is not considered multi-factor authentication. A replay attack is when an attacker intercepts a communication and replays it on the network. Anti-replay mechanisms help ensure that each authentication is unique.",
    },
    {
        "identifier": "8.6.1",
        "domain": DOMAIN_8,
        "description": "If accounts used by systems or applications can be used for interactive login, they are managed as follows: Interactive use is prevented unless needed for an exceptional circumstance; Interactive use is limited to the time needed for the exceptional circumstance; Business justification for interactive use is documented; Interactive use is explicitly approved by management; Individual user identity is confirmed before access to account is granted; Every action taken is attributable to an individual user.",
        "guidance": "Like individual user accounts, system and application accounts require accountability. If an environment is set up so that systems or applications can be used interactively, and the account has been set up with generic or shared credentials, it may be impossible to identify and trace the actions taken by any specific individual. Limiting interactive logins to only specific circumstances and managing those accounts strictly when interactive login is required helps to prevent unauthorized individuals from logging in and using the same account. Where possible, interactive logins should be restricted to prevent unauthorized use.",
    },
    {
        "identifier": "8.6.2",
        "domain": DOMAIN_8,
        "description": "Passwords/passphrases for any application and system accounts that can be used for interactive login are not hard coded in scripts, configuration/property files, or bespoke and custom source code.",
        "guidance": "Hard-coding passwords and passphrases, especially if maintained by applications and system accounts, can create security weaknesses, especially if those accounts can be used for interactive login. If a malicious individual discovers and accesses the files, the hard-coded passwords and passphrases are compromised. Confirming that deletions can be particularly difficult to implement. For example, consider implementing built-in management for security of authentication factors for application and system accounts.",
    },
    {
        "identifier": "8.6.3",
        "domain": DOMAIN_8,
        "description": "Passwords/passphrases for any application and system accounts are protected against misuse as follows: Passwords/passphrases are changed periodically (at the frequency defined in the entity's targeted risk analysis, which is performed in accordance with all elements specified in Requirement 12.3.1) and upon suspicion or confirmation of compromise; Passwords/passphrases are constructed with sufficient complexity appropriate for how frequently the entity changes the passwords/passphrases.",
        "guidance": "Application and system accounts pose a greater inherent security risk than user accounts because they often run in an elevated security context, with access to systems that would not be appropriate for a regular user account. They also may be shared across multiple systems, and controls may be more difficult to implement. Application and system accounts also pose additional risk because the passwords/passphrases are often hard-coded and embedded. Entities should consider the following risk factors when determining how frequently to change and the complexity of passwords/passphrases: how securely the passwords/passphrases are stored; whether the account is used interactively; the number of people with access to the password; how frequently changes can be implemented and tested without breaking functionality; turnover; and staff knowledge.",
    },
    # ── Requirement 9 (pages 172-197) ──
    {
        "identifier": "9.1.1",
        "domain": DOMAIN_9,
        "description": "All security policies and operational procedures that are identified in Requirement 9 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 9.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 9. While it is important to define the specific policies or procedures called out in Requirement 9, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "9.1.2",
        "domain": DOMAIN_9,
        "description": "Roles and responsibilities for performing activities in Requirement 9 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "9.2.1",
        "domain": DOMAIN_9,
        "description": "Appropriate facility entry controls are in place to restrict physical access to systems in the CDE.",
        "guidance": "Without physical access controls, unauthorized individuals could potentially gain access to the CDE and sensitive information, or could alter an entity's system configuration, introduce vulnerabilities into the network, or destroy or steal equipment. Facility entry controls include physical security controls such as badge readers or other mechanisms such as lock and key with a current list of all individuals having the keys.",
    },
    {
        "identifier": "9.2.1.1",
        "domain": DOMAIN_9,
        "description": "Individual physical access to sensitive areas within the CDE is monitored with either video cameras or physical access control mechanisms (or both) as follows: Entry/exit points to/from sensitive areas within the CDE are monitored; Monitoring devices or mechanisms are protected from tampering or disabling; Collected data is reviewed and correlated with other entries.",
        "guidance": "Monitoring the entry and exit of individuals to/from sensitive areas helps identify individuals entering and leaving sensitive areas, as well as when they entered and exited. Installing cameras and/or physical access control mechanisms at entry/exit points to sensitive areas can help detect unauthorized physical access. When used in combination with physical access controls, video cameras can also help correlate physical access with electronic access events. Cameras should be positioned so they are not easily tampered with or disabled, so they do not have blind spots, and so they are able to detect suspicious activity within the area.",
    },
    {
        "identifier": "9.2.2",
        "domain": DOMAIN_9,
        "description": "Physical and/or logical controls are implemented to restrict use of publicly accessible network jacks within the facility.",
        "guidance": "Restricting access to network jacks (or network ports) will prevent malicious individuals from plugging into readily available network jacks and gaining access to the CDE. Using physical and/or logical controls, such as disabling network jacks, and only enabling them when explicitly authorized, or limiting access to publicly accessible network areas, can help prevent an unauthorized person from connecting to the entity's network resources.",
    },
    {
        "identifier": "9.2.3",
        "domain": DOMAIN_9,
        "description": "Physical access to wireless access points, gateways, networking/communications hardware, and telecommunication lines within the facility is restricted.",
        "guidance": "Without appropriate physical security over access to wireless components and devices, and computer networking and telecommunications equipment and lines, malicious users could gain access to the entity's network resources. Additionally, they could connect their own devices to the network to gain unauthorized access to the CDE or communications infrastructure.",
    },
    {
        "identifier": "9.2.4",
        "domain": DOMAIN_9,
        "description": "Access to consoles in sensitive areas is restricted via locking when not in use.",
        "guidance": "Locking consoles when not in use prevents unauthorized individuals from gaining access to sensitive information, altering system configurations, introducing vulnerabilities into the network, or destroying records.",
    },
    {
        "identifier": "9.3.1",
        "domain": DOMAIN_9,
        "description": "Procedures are implemented for authorizing and managing physical access of personnel to the CDE, including: Identifying personnel; Managing changes to an individual's physical access requirements; Revoking or terminating personnel identification; Limiting access to the identification process or system to authorized personnel.",
        "guidance": "Establishing procedures for granting, managing, and removing physical access for authorized personnel ensures that access is controlled and only given to those with a valid business need. It is important to visually identify the personnel that are physically present and to determine whether they have authorized access. One way to identify personnel is to assign them badges.",
    },
    {
        "identifier": "9.3.1.1",
        "domain": DOMAIN_9,
        "description": "Physical access to sensitive areas within the CDE for personnel is controlled as follows: Access is authorized and based on individual job function; Access is revoked immediately upon termination; All physical access mechanisms, such as keys, access cards, etc., are returned or disabled immediately upon termination.",
        "guidance": "Controlling physical access to sensitive areas helps ensure that only authorized personnel with a legitimate business need are granted access. Where possible, organizations should have policies and procedures to ensure that before physical access is granted to sensitive areas, access mechanisms are returned, or disabled, as soon as possible upon their departure. This will ensure that once their employment has ended, all physical access mechanisms are immediately disabled or revoked.",
    },
    {
        "identifier": "9.3.2",
        "domain": DOMAIN_9,
        "description": "Procedures are implemented for authorizing and managing visitor access to the CDE, including: Visitors are authorized before entering; Visitors are escorted at all times; Visitors are clearly identified and given a badge or other identification that visibly distinguishes visitors from personnel; Visitor badges or other identification expire.",
        "guidance": "Visitor controls are important to reduce the ability of unauthorized and malicious persons to gain access to facilities and potentially to cardholder data. Visitor controls ensure visitors are identifiable as visitors so personnel can monitor their activities, and that their access is restricted to just the duration of their legitimate visit.",
    },
    {
        "identifier": "9.3.3",
        "domain": DOMAIN_9,
        "description": "Visitor badges or identification are surrendered or deactivated before visitors leave the facility or at the date of expiration.",
        "guidance": "Ensuring that visitor badges are returned or deactivated upon expiry or completion of the visit prevents malicious persons from using a previously authorized pass to gain physical access into the building after the visit has ended.",
    },
    {
        "identifier": "9.3.4",
        "domain": DOMAIN_9,
        "description": "A visitor log is used to maintain a physical audit trail of visitor activity, including: The visitor's name and the organization represented; The date and time of the visit; The name of the personnel authorizing physical access; Retaining the log for at least three months, unless otherwise restricted by law.",
        "guidance": "A visitor log documenting minimum information about the visitor is easy and inexpensive to maintain and will assist in identifying physical access to a building or room, and potential access to cardholder data. When logging the date and time of visit, including both in and out times is considered a best practice. Having information about visitors at the end of the visit, including both in and out times is considered a best practice. Also it is good to track if visitors left the building or have been escorted through the entire visit.",
    },
    {
        "identifier": "9.4.1",
        "domain": DOMAIN_9,
        "description": "All media with cardholder data is physically secured.",
        "guidance": "Controls for physically securing media are intended to prevent unauthorized persons from gaining access to cardholder data on any type of media. Cardholder data is susceptible to unauthorized viewing, copying, or scanning if it is unprotected while it is on removable or portable media, printed out, or left on someone's desk.",
    },
    {
        "identifier": "9.4.1.1",
        "domain": DOMAIN_9,
        "description": "Offline media backups with cardholder data are stored in a secure location.",
        "guidance": "If stored in a non-secured facility, backups containing cardholder data may easily be lost, stolen, or copied for malicious intent. For the secure storage of backup media, a good practice is to store media in an off-site facility, such as an alternate or backup site or commercial storage facility.",
    },
    {
        "identifier": "9.4.1.2",
        "domain": DOMAIN_9,
        "description": "The security of the offline media backup location(s) with cardholder data is reviewed at least once every 12 months.",
        "guidance": "Performing regular reviews of the storage facility enables the organization to address identified security issues promptly, minimizing the potential risk. It is a good practice to continuously review the security of the area where media is being stored to ensure that security remains adequate.",
    },
    {
        "identifier": "9.4.2",
        "domain": DOMAIN_9,
        "description": "All media with cardholder data is classified in accordance with the sensitivity of the data.",
        "guidance": "Media not identified as confidential may not be adequately protected or may be lost or stolen. It is important that media be identified such that its classification status is apparent. Media not identified as confidential may not be adequately protected and may be lost or stolen.",
    },
    {
        "identifier": "9.4.3",
        "domain": DOMAIN_9,
        "description": "Media with cardholder data sent outside the facility is secured as follows: Media is logged; Media is sent by secured courier or other delivery method that can be accurately tracked; Management approves any and all media that is sent outside the facility (including when media is distributed to individuals).",
        "guidance": "Media may be lost or stolen if sent via a non-trackable method such as regular postal mail. The use of secure couriers to deliver any media that contains cardholder data allows organizations to use their tracking systems to maintain inventory and location of shipments.",
    },
    {
        "identifier": "9.4.4",
        "domain": DOMAIN_9,
        "description": "Management approves all media with cardholder data that is moved outside the facility (including when media is distributed to individuals).",
        "guidance": "Having a firm process for ensuring that all media movements are approved before the media is removed from secure areas minimizes the risk of the media being lost or stolen. Without a firm process, media movements are not tracked and the media's whereabouts would be unknown, leading to lost or stolen media.",
    },
    {
        "identifier": "9.4.5",
        "domain": DOMAIN_9,
        "description": "Inventory logs of all electronic media with cardholder data are maintained.",
        "guidance": "Without careful inventory methods and storage controls, stolen or missing electronic media could go unnoticed for an indefinite amount of time.",
    },
    {
        "identifier": "9.4.5.1",
        "domain": DOMAIN_9,
        "description": "Inventories of electronic media with cardholder data are conducted at least once every 12 months.",
        "guidance": "Without careful inventory methods and storage controls, stolen or missing electronic media could go unnoticed for an indefinite amount of time. Performing regular inventories of electronic media helps ensure that the entity can identify lost or missing electronic media.",
    },
    {
        "identifier": "9.4.6",
        "domain": DOMAIN_9,
        "description": "Hard-copy materials with cardholder data are destroyed when no longer needed for business or legal reasons, as follows: Materials are cross-cut shredded, incinerated, or pulped so that cardholder data cannot be reconstructed; Materials are stored in secure storage containers prior to destruction.",
        "guidance": "If steps are not taken to destroy information contained on hard-copy media before disposal, malicious individuals may retrieve information from the disposed media, leading to a data compromise. For example, malicious individuals may use a technique known as dumpster diving, where they search through trashcans and recycle bins for information they can use to launch an attack. Securing storage containers used for materials that are going to be destroyed prevents sensitive information from being captured while the materials are being collected.",
    },
    {
        "identifier": "9.4.7",
        "domain": DOMAIN_9,
        "description": "Electronic media with cardholder data is destroyed when no longer needed for business or legal reasons via one of the following: The electronic media is destroyed; The electronic media is rendered unrecoverable so that cardholder data cannot be reconstructed.",
        "guidance": "If steps are not taken to destroy information contained on electronic media when no longer needed, malicious individuals may retrieve information from the disposed media, leading to a data compromise. For example, malicious individuals may use a technique known as dumpster diving, where they search through trashcans and recycle bins for information. The deletion function in most operating systems allows deleted data to be recovered, so instead a dedicated secure deletion function or application should be used to make data unrecoverable.",
    },
    {
        "identifier": "9.5.1",
        "domain": DOMAIN_9,
        "description": "POI devices that capture payment card data via direct physical interaction with the payment card form factor are protected from tampering and unauthorized substitution, including the following: Maintaining a list of POI devices; Periodically inspecting POI device surfaces to detect tampering or unauthorized substitution; Training personnel to be aware of suspicious behavior and to report tampering or unauthorized substitution of devices.",
        "guidance": "Criminals attempt to steal payment card data by stealing and/or manipulating card-reading devices and terminals. They will also try to add skimming components to the outside of devices, which are designed to capture payment card data before it enters the device. They can also try to insert card-reading software components inside the device once the criminals have gained physical access to the device. They may also try to intercept payment card data after it has been read by the device, for example by redirecting payment card data to a different destination.",
    },
    {
        "identifier": "9.5.1.1",
        "domain": DOMAIN_9,
        "description": "An up-to-date list of POI devices is maintained, including: Make and model of the device; Location of device; Device serial number or other method of unique identification.",
        "guidance": "Keeping an up-to-date list of POI devices helps an organization track where devices are supposed to be and quickly identify if a device is missing or lost. Methods for maintaining a list of devices may be automated (for example, a device-management system) or manual (for example, documented in electronic or paper records). For the list, entities should also consider whether there are other relevant details about the device that could help with identification.",
    },
    {
        "identifier": "9.5.1.2",
        "domain": DOMAIN_9,
        "description": "POI device surfaces are periodically inspected to detect tampering and unauthorized substitution.",
        "guidance": "Regular inspections of devices will help organizations detect tampering more quickly via external evidence—for example, the addition of a card skimmer—or replacement of a device, thereby minimizing the potential impact of using fraudulent devices. Methods for periodic inspection include checking the serial number or other device characteristics and comparing the information to the list of known devices to verify the device has not been swapped with a fraudulent device.",
    },
    {
        "identifier": "9.5.1.2.1",
        "domain": DOMAIN_9,
        "description": "The frequency of periodic POI device inspections and the type of inspections performed is defined in the entity's targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1.",
        "guidance": "Entities should determine the optimum frequency of POI device inspections based on the environment in which the device operates. The frequency of inspections will depend on factors such as the location of a device and whether the device is attended or unattended. For example, devices left in public areas without supervision by the entity's personnel may have more frequent inspections than devices kept in secure areas or that are supervised. In addition, many POI vendors include guidance in their documentation and recommendations for the frequency and type of inspections.",
    },
    {
        "identifier": "9.5.1.3",
        "domain": DOMAIN_9,
        "description": "Training is provided for personnel in POI environments to include the following: Verifying the identity of any third-party persons claiming to be repair or maintenance personnel, before granting them access to modify or troubleshoot devices; Not installing, replacing, or returning devices without verification; Being aware of suspicious behavior around devices; Reporting suspicious behavior and indications of device tampering or substitution to appropriate personnel.",
        "guidance": "Criminals will often pose as authorized maintenance personnel in order to gain access to POI devices. Personnel training should include being alert to and questioning anyone who shows up to do work on POI devices to ensure they are who they say they are. Another trick criminals use is to send a new device with instructions for swapping it with a legitimate device and to send the legitimate device to an address where the criminal then has possession of it. Personnel should always verify with their manager or supplier that the device is legitimate and came from a trusted source before installing it or using it for business.",
    },
    # ── Requirement 10 (pages 198-208) ──
    {
        "identifier": "10.1.1",
        "domain": DOMAIN_10,
        "description": "All security policies and operational procedures that are identified in Requirement 10 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 10.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 10. While it is important to define the specific policies or procedures called out in Requirement 10, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "10.1.2",
        "domain": DOMAIN_10,
        "description": "Roles and responsibilities for performing activities in Requirement 10 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "10.2.1",
        "domain": DOMAIN_10,
        "description": "Audit logs are enabled and active for all system components and cardholder data.",
        "guidance": "Audit logs must be enabled for all system components. Audit log data alerts the system administrator, provides data to other monitoring mechanisms, and provides a history trail for post-incident follow-up. Logging and analyzing security-relevant events enables an entity to identify and trace potentially malicious activities. When an entity considers which information should be protected in its audit logs, it is important to consider that information deemed to be sensitive should be protected in the audit logs to maintain confidentiality.",
    },
    {
        "identifier": "10.2.1.1",
        "domain": DOMAIN_10,
        "description": "Audit logs capture all individual user access to cardholder data.",
        "guidance": "It is critical to have a process or system that links user access to the system components accessed. Malicious individuals could obtain knowledge of a user account with access to systems in the CDE, or they could create a new, unauthorized account in order to access cardholder data. A record of all individual access to cardholder data can identify which accounts may have been compromised or misused.",
    },
    {
        "identifier": "10.2.1.2",
        "domain": DOMAIN_10,
        "description": "Audit logs capture all actions taken by any individual with administrative access, including any interactive use of application or system accounts.",
        "guidance": "Accounts with increased access privileges, such as the administrator or root account, have the potential to greatly impact the security of a system. Without a log of the activities performed, an organization is unable to trace any issues resulting from an administrative error or misuse of privilege back to the specific action and individual.",
    },
    {
        "identifier": "10.2.1.3",
        "domain": DOMAIN_10,
        "description": "Audit logs capture all access to audit logs.",
        "guidance": "Users with access to audit logs may attempt to use their access to hide their actions. A record of all access allows an entity to identify any issues with the access controls and to detect potential security incidents.",
    },
    {
        "identifier": "10.2.1.4",
        "domain": DOMAIN_10,
        "description": "Audit logs capture all invalid logical access attempts.",
        "guidance": "Malicious individuals will often perform multiple access attempts on targeted systems. Multiple invalid login attempts may be an indication of an unauthorized user's attempts to brute force or guess a password.",
    },
    {
        "identifier": "10.2.1.5",
        "domain": DOMAIN_10,
        "description": "Audit logs capture all changes to identification and authentication credentials including, but not limited to: Creation of new accounts; Elevation of privileges; All changes, additions, or deletions to accounts with administrative access.",
        "guidance": "Logging changes to authentication credentials (including elevation of privileges, additions, and deletions of accounts with root or administrative access) provides evidence of activities. Malicious users may attempt to manipulate authentication credentials to bypass them or impersonate a valid account.",
    },
    {
        "identifier": "10.2.1.6",
        "domain": DOMAIN_10,
        "description": "Audit logs capture the following: All initialization of new audit logs, and All starting, stopping, or pausing of the existing audit logs.",
        "guidance": "Turning off or pausing audit logs before performing illicit activities is a common practice for malicious users who want to avoid detection. Initialization of audit logs could indicate that the log function was disabled by a user to hide their actions.",
    },
    {
        "identifier": "10.2.1.7",
        "domain": DOMAIN_10,
        "description": "Audit logs capture all creation and deletion of system-level objects.",
        "guidance": "Malicious software, such as malware, often creates or replaces system-level objects on the target system to control a particular function or operation on that system. By logging when system-level objects are created or deleted, it will be easier to determine whether such modifications were authorized.",
    },
    {
        "identifier": "10.2.2",
        "domain": DOMAIN_10,
        "description": "Audit logs record the following details for each auditable event: User identification; Type of event; Date and time; Success and failure indication; Origination of event; Identity or name of affected data, system component, resource, or service (for example, name and protocol).",
        "guidance": "By recording these details for the auditable events at 10.2.1.1 through 10.2.1.7, a potential compromise can be quickly identified, and with sufficient detail to facilitate follow-up on suspicious activities.",
    },
    {
        "identifier": "10.3.1",
        "domain": DOMAIN_10,
        "description": "Read access to audit logs files is limited to those with a job-related need.",
        "guidance": "Audit logs contain sensitive information, and read access to audit logs must be limited to only those with a valid business need. This access includes audit logs on all system components, including those for security, application, and operating system functions, and data logs. Adequate protection of the audit logs includes strong access control (limiting access to logs based on need to know only) and use of physical or network segregation to make the logs difficult to find and modify.",
    },
    {
        "identifier": "10.3.2",
        "domain": DOMAIN_10,
        "description": "Audit log files are protected to prevent modifications by individuals.",
        "guidance": "Often a malicious individual who has entered the network will try to edit the audit logs to hide their activity. Without adequate protection of audit logs, their completeness, accuracy, and integrity cannot be guaranteed, and the audit logs can be rendered useless as an investigation tool after a compromise. Therefore, audit logs should be protected from being modified to maintain their integrity.",
    },
    {
        "identifier": "10.3.3",
        "domain": DOMAIN_10,
        "description": "Audit log files, including those for external-facing technologies, are promptly backed up to a secure, central, internal log server(s) or other media that is difficult to modify.",
        "guidance": "Promptly backing up the logs to a centralized log server or media that is difficult to alter keeps the logs protected even if the system generating the logs becomes compromised. Writing logs from external-facing technologies such as wireless, firewalls, DNS, and mail servers reduces the risk of those logs being lost or altered. Logs may be written directly, or offloaded or copied from external systems to the secure internal system or media.",
    },
    {
        "identifier": "10.3.4",
        "domain": DOMAIN_10,
        "description": "File integrity monitoring or change-detection mechanisms is used on audit logs to ensure that existing log data cannot be changed without generating alerts.",
        "guidance": "File integrity monitoring or change-detection systems check for changes to critical files and notify when such changes are detected. For file integrity monitoring purposes, an entity usually monitors files that don't regularly change, but when changed indicate a possible compromise. Automated monitoring for changes to audit log files using file integrity monitoring or change-detection tools helps ensure that existing log data cannot be changed without generating an alert.",
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
