import csv
import os

OUTPUT = r"c:\Users\PC\Desktop\Control Outputs\PCI_Controls_Preview.csv"

DOMAIN_6 = "Requirement 6: Develop and Maintain Secure Systems and Software"
DOMAIN_7 = "Requirement 7: Restrict Access to System Components and Cardholder Data by Business Need to Know"
DOMAIN_8 = "Requirement 8: Identify Users and Authenticate Access to System Components"

existing_count = 0
if os.path.exists(OUTPUT):
    with open(OUTPUT, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row and row[0]:
                existing_count += 1

controls = [
    # ── Requirement 6 continued (pages 111-122) ──
    {
        "identifier": "6.3.3.1",
        "domain": DOMAIN_6,
        "description": "The frequency of patches/updates to address known vulnerabilities is defined in the entity's targeted risk analysis, which is performed in accordance with all elements specified in Requirement 12.3.1.",
        "guidance": "Entities determine the optimum period to undertake periodic evaluations based on criteria such as the complexity of each entity's environment and the number and types of systems that need to be evaluated.",
    },
    {
        "identifier": "6.4.1",
        "domain": DOMAIN_6,
        "description": "For public-facing web applications, new threats and vulnerabilities are addressed on an ongoing basis and these applications are protected against known attacks as follows: Reviewing public-facing web applications via manual or automated application vulnerability security assessment tools or methods, at least once every 12 months and after significant changes; OR Installing an automated technical solution(s) that continually detects and prevents web-based attacks.",
        "guidance": "Public-facing web applications are primary targets for attackers, and poorly coded web applications provide an easy path for attackers to gain access to sensitive data and systems. These applications are primarily targets not only for external attackers but also for insiders. When using automated technical solutions, it is important to include the capability to generate alerts to ensure that any detected attacks can be investigated. A web application firewall (WAF) installed in front of public-facing web applications to check all traffic is an example of an automated technical solution that detects and prevents web-based attacks.",
    },
    {
        "identifier": "6.4.2",
        "domain": DOMAIN_6,
        "description": "For public-facing web applications, an automated technical solution is deployed that continually detects and prevents web-based attacks, with at least the following: Is installed in front of public-facing web applications and is configured to detect and prevent web-based attacks; Actively running and up to date as applicable; Generating audit logs; Configured to either block web-based attacks or generate an alert that is immediately investigated.",
        "guidance": "Attacks on public-facing web applications are primary targets for attackers, and poorly coded web applications provide an easy path for attackers. When using automated technical solutions, it is important to include the capability to generate alerts to ensure that any detected attacks can be investigated. A web application firewall (WAF) installed in front of public-facing web applications to check all traffic is an example of an automated technical solution. A properly configured WAF helps to prevent application-layer attacks on applications.",
    },
    {
        "identifier": "6.4.3",
        "domain": DOMAIN_6,
        "description": "All payment page scripts that are loaded and executed in the consumer's browser are managed as follows: A method is implemented to confirm that each script is authorized; A method is implemented to assure the integrity of each script; An inventory of all scripts is maintained with written justification as to why each is necessary.",
        "guidance": "Scripts loaded and executed in the payment page can have their functionality altered without the entity's knowledge and can also have the functionality to load additional external scripts. Such scripts can be used to skim payment data from the consumer's browser. Ensuring that scripts have been specifically approved prevents unauthorized scripts from being added to the payment page. Using techniques to prevent tampering with the script will minimize the probability of the script being modified to carry out unauthorized behavior, such as skimming the cardholder data from the payment page.",
    },
    {
        "identifier": "6.5.1",
        "domain": DOMAIN_6,
        "description": "Changes to all system components in the production environment are made according to established procedures that include: Documentation of impact; Documented change approval by authorized parties; Functionality testing to verify that the change does not adversely impact the security of the system; Backout procedures; Requirement 6.2.2 is applied to all changes; Procedures to address failures and return to a secure state; Testing to verify that the change does not adversely impact the security of system security.",
        "guidance": "Change management procedures must be applied to all changes—including addition, removal, or modification of any system component—in the production environment. It is important to have documented procedures that define how changes are controlled, including how backout procedures are implemented. For each change, it is important to have documented procedures that address failures and provide the ability to restore the system to its previous secure state. For each change, it is important to have procedures that address how to return to the previous secure state.",
    },
    {
        "identifier": "6.5.2",
        "domain": DOMAIN_6,
        "description": "Upon completion of a significant change, all applicable PCI DSS requirements are confirmed to be in place on all new or changed systems and networks, and documentation is updated as applicable.",
        "guidance": "Having processes for analyzing significant changes helps ensure that all appropriate PCI DSS controls are applied to any systems or networks added or changed within the in-scope environment, and that PCI DSS requirements continue to be met to secure the environment. Building this validation into change management processes helps ensure that device inventories and configuration standards are kept up to date and security controls are applied where needed.",
    },
    {
        "identifier": "6.5.3",
        "domain": DOMAIN_6,
        "description": "Pre-production environments are separated from production environments and the separation is enforced with access controls.",
        "guidance": "Due to the constantly changing state of pre-production environments, they are often less secure than the production environment. Organizations must clearly understand which environments are test environments or development environments and how those are separated from production. The purpose of separating roles and functions between production and pre-production environments is to reduce the number of personnel with access to the production environment and thereby minimize risk.",
    },
    {
        "identifier": "6.5.4",
        "domain": DOMAIN_6,
        "description": "Roles and functions are separated between production and pre-production environments to provide accountability such that only reviewed and approved changes are deployed.",
        "guidance": "The intent of separating roles and functions between production and pre-production environments is to reduce the number of personnel with access to the production environment and thereby minimize the risk of unauthorized, unintentional, or inappropriate access to critical data and production functions. The intent of this control is to separate critical activities to provide oversight and review to catch errors and to minimize the chances of fraud or theft, since two people would need to collude in order to hide an activity.",
    },
    {
        "identifier": "6.5.5",
        "domain": DOMAIN_6,
        "description": "Live PANs are not used in pre-production environments, except where those environments are included in the CDE and protected in accordance with all applicable PCI DSS requirements.",
        "guidance": "Use of live PANs outside of protected CDEs provides malicious individuals with the opportunity to gain unauthorized access to cardholder data. Live PANs refer to valid PANs (not test PANs) issued by a payment brand. Additionally, PANs that result in a different hash of a payment brand, or that are used in a training test will be treated as live PANs. All PAN data must be identified as a live PAN and purged from the test environment before they are excluded from PCI DSS that PANs are not live.",
    },
    {
        "identifier": "6.5.6",
        "domain": DOMAIN_6,
        "description": "Test data and test accounts are removed from system components before the system goes into production.",
        "guidance": "Test data may give away information about the functioning of an application or system and is an easy target for unauthorized individuals to exploit. Removal of test data and accounts before a system goes into production helps ensure that this information could not be used by unauthorized individuals.",
    },
    # ── Requirement 7 (pages 123-135) ──
    {
        "identifier": "7.1.1",
        "domain": DOMAIN_7,
        "description": "All security policies and operational procedures that are identified in Requirement 7 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 7.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 7. While it is important to define the specific policies or procedures called out in Requirement 7, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "7.1.2",
        "domain": DOMAIN_7,
        "description": "Roles and responsibilities for performing activities in Requirement 7 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "7.2.1",
        "domain": DOMAIN_7,
        "description": "An access control model is defined and includes granting access as follows: Appropriate access depending on the entity's business and access needs; Access to system components and data resources that is based on users' job classification and function; The least privileges required (for example, user, administrator) to perform a job function.",
        "guidance": "Defining an access control model that is appropriate for the entity's technology and access control philosophy supports a consistent and uniform way of assigning access and reduces the possibility of errors such as the granting of excessive rights. It is beneficial for duties to be clearly defined between IT and information system support functions. In particular, establishing roles such as programming, database administration, system management, and network management will help to define the scope of duties and responsibilities. The separation of duties provides that no single individual has end-to-end control of a process without an independent checkpoint or oversight.",
    },
    {
        "identifier": "7.2.2",
        "domain": DOMAIN_7,
        "description": "Access is assigned to users, including privileged users, based on: Job classification and function; Least privileges necessary to perform job responsibilities.",
        "guidance": "Assigning least privileges helps prevent users without sufficient knowledge about the application from incorrectly or accidentally changing application configuration or altering its security settings. Enforcing least privilege also helps to minimize the scope of damage if an unauthorized person gains access to a user ID. Access rights are granted to a user by assignment and are based on the specific user function and the minimum access needed to perform that function. Entities should consider using Privileged Access Management (PAM), which is a method to grant access to privileged accounts only when those privileges are needed, by immediately revoking that access once they are no longer needed.",
    },
    {
        "identifier": "7.2.3",
        "domain": DOMAIN_7,
        "description": "Required privileges are approved by authorized personnel.",
        "guidance": "Documented approval (for example, in writing or electronically) assures that those with access and privileges are known and authorized by management, and that their access is necessary for their job function.",
    },
    {
        "identifier": "7.2.4",
        "domain": DOMAIN_7,
        "description": "All user accounts and related access privileges, including third-party/vendor accounts, are reviewed as follows: At least once every six months; To ensure user accounts and access remain appropriate based on job function; Any inappropriate access is addressed; Management acknowledges that access remains appropriate.",
        "guidance": "Regular review of access rights helps to detect excessive access rights remaining after user job responsibilities change, system functions change, or other modifications. This review provides another opportunity to ensure that any previously granted access to all terminated users has been revoked and that any unauthorized changes have been addressed. When a user transfers into a new role or a new department, typically the privileges and access associated with their former role are no longer required. Quarterly review, both making incremental updates to access as needed and performing a full review at least once every 6 months, helps minimize access creep.",
    },
    {
        "identifier": "7.2.5",
        "domain": DOMAIN_7,
        "description": "All application and system accounts and related access privileges are assigned and managed as follows: Based on the least privileges necessary for the operability of the system or application; Access is limited to the systems, applications, or processes that specifically require their use.",
        "guidance": "It is important to establish the appropriate access level for application or system accounts. If such accounts are compromised, malicious users will receive the same access level as that granted to the application or system. Therefore, it is important to ensure limited access is granted to the application or system. Some best practices to consider for application establishing a baseline when setting up these application accounts include: making sure that the account is not a member of a privileged group; restricting which computers the account can be used on; restricting use of local sign-on rights; and removing any additional settings like VPN access and remote access.",
    },
    {
        "identifier": "7.2.5.1",
        "domain": DOMAIN_7,
        "description": "All access by application and system accounts and related access privileges are reviewed as follows: Periodically (at the frequency defined in the entity's targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1); The application/system access remains appropriate for the function being performed; Any inappropriate access is addressed; Management acknowledges that access remains appropriate.",
        "guidance": "Regular review of access rights helps to detect excessive access rights remaining after system functions change or other modifications. This review also provides another opportunity to ensure that access for all terminated users has been removed when no longer needed, and that they may be used by malicious parties for unauthorized access.",
    },
    {
        "identifier": "7.2.6",
        "domain": DOMAIN_7,
        "description": "All user access to query repositories of stored cardholder data is restricted as follows: Via applications or other programmatic methods, with access and allowed actions based on user roles and least privileges; Only the responsible administrator(s) can directly access or query repositories of stored cardholder data.",
        "guidance": "The misuse of query access to repositories of cardholder data has been a regular cause of data breaches. Limiting such access to administrators reduces the risk of such access being abused by unauthorized users. Entities should consider restricting the scope of privilege, including creating, altering, rotating, distributing, or otherwise maintaining encryption keys. Also consider including the scope of access to cardholder data elements, files, tables, logs, indices, views, and all other data elements that contain cardholder data to only those user that are needed to perform their job functions.",
    },
    {
        "identifier": "7.3.1",
        "domain": DOMAIN_7,
        "description": "An access control system(s) is in place that restricts access based on a user's need to know and covers all system components.",
        "guidance": "Without a mechanism to restrict access based on a user's need to know, a user may unknowingly be granted access to cardholder data. Access control systems automate the process of restricting access and assigning privileges.",
    },
    {
        "identifier": "7.3.2",
        "domain": DOMAIN_7,
        "description": "The access control system(s) is configured to enforce permissions assigned to individuals, applications, and systems based on job classification and function.",
        "guidance": "Having privilege levels provides the entity with the ability for more granular control over allowing errors or the opportunity for unauthorized access in the assignment of permissions to individuals, applications, and systems.",
    },
    {
        "identifier": "7.3.3",
        "domain": DOMAIN_7,
        "description": "The access control system(s) is set to 'deny all' by default.",
        "guidance": "A default setting of 'deny all' ensures no one is granted access until and unless a rule is established specifically granting such access. Entities may want to consider how access permissions are assigned, including how permissions are inherited, and how access is granted via security groups or the use of 'deny all' in combination with other rules.",
    },
    # ── Requirement 8 (pages 136-158) ──
    {
        "identifier": "8.1.1",
        "domain": DOMAIN_8,
        "description": "All security policies and operational procedures that are identified in Requirement 8 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 8.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 8. While it is important to define the specific policies or procedures called out in Requirement 8, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For this reason, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "8.1.2",
        "domain": DOMAIN_8,
        "description": "Roles and responsibilities for performing activities in Requirement 8 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "8.2.1",
        "domain": DOMAIN_8,
        "description": "All users are assigned a unique ID before access to system components or cardholder data is allowed.",
        "guidance": "The ability to trace actions performed on a computer system to an individual is fundamental to the ability to hold users accountable and traceability and is fundamental to establishing effective access controls. By ensuring each user is uniquely identified, instead of using one ID for several employees, an organization can maintain individual responsibility for actions and an effective audit trail per employee. In addition, this will assist with incident management when a malicious or inadvertent event occurs.",
    },
    {
        "identifier": "8.2.2",
        "domain": DOMAIN_8,
        "description": "Group, shared, or generic accounts, or other shared authentication credentials are only used when necessary on an exception basis, and are managed as follows: Account use is prevented unless needed for an exceptional circumstance; Use is limited to the time needed for the exceptional circumstance; Business justification for use is documented; Use is explicitly approved by management; Individual user identity is confirmed before access to account is granted.",
        "guidance": "If multiple users share the same authentication credentials (for example, user account and password), it becomes impossible to trace system access and activities to an individual, and therefore, it becomes impossible to trace fraudulent activities to a specific user, for having effective logging of an individual's activities. The ability to associate individuals with the actions performed with the shared ID becomes impossible to determine who performed an action, what action was performed, and when. If shared IDs are used for any reason, strong management controls need to be established to maintain individual accountability.",
    },
    {
        "identifier": "8.2.3",
        "domain": DOMAIN_8,
        "description": "Additional requirement for service providers: Service providers with remote access to customer premises use unique authentication factors for each customer premises.",
        "guidance": "Service providers with remote access to customer premises typically use this access to support PCI DSS compliance functions. If a service provider uses the same authentication factors to access multiple customers, all the customers can easily be compromised if an attacker compromises that one credential. Tools, policies, and procedures can help ensure that service providers use unique authentication factors for remote access to customer premises.",
    },
    {
        "identifier": "8.2.4",
        "domain": DOMAIN_8,
        "description": "Addition, deletion, and modification of user IDs, authentication factors, and other identifier objects are managed as follows: Authorized with the appropriate approval; Implemented with only the privileges specified on the documented approval.",
        "guidance": "Controlling the lifecycle of a user ID (additions, deletions, and modifications) ensures that only authorized individuals with the expected privilege levels can access the system. When user IDs are created outside of or not managed in accordance with the documented approval process, the user IDs may be created without appropriate privilege levels or background checks, or they may not be associated with the appropriate authorization.",
    },
    {
        "identifier": "8.2.5",
        "domain": DOMAIN_8,
        "description": "Access for terminated users is immediately revoked.",
        "guidance": "If an employee or third-party/vendor has left the company and still has access to the network via their user account, unnecessary or malicious access to cardholder data could occur—either by the former employee or by a malicious user who exploits the old and/or unused account. To prevent unauthorized access, user credentials and other authentication methods therefore need to be revoked promptly upon the departure of any user who no longer requires access.",
    },
    {
        "identifier": "8.2.6",
        "domain": DOMAIN_8,
        "description": "Inactive user accounts are removed or disabled within 90 days of inactivity.",
        "guidance": "Accounts that are not used regularly are often targets of attack since it is less likely that any changes, such as a changed password, will be noticed. Not being actively used, that is, accounts that have had no activity for 90 days, should be disabled or removed as soon as it is feasible to do so. Where it may be reasonably anticipated that an account will not be used for an extended period of time, the account should be disabled as soon as the leave begins, rather than waiting 90 days.",
    },
    {
        "identifier": "8.2.7",
        "domain": DOMAIN_8,
        "description": "Accounts used by third parties to access, support, or maintain system components via remote access are managed as follows: Enabled only during the time period needed and disabled when not in use; Use is monitored for unexpected activity.",
        "guidance": "Allowing vendors to have 24/7 access into the network in case they need to support or maintain systems increases the chances of unauthorized access, either from a user in the vendor's environment or from a malicious individual who finds and uses this always-available external entry point into the network. Enabling access only for the time periods needed and monitoring it while in use helps to limit these exposures. When third parties need to access the entity's systems, it is important to ensure that access is granted for only the duration needed and is disabled or removed when no longer in use.",
    },
    {
        "identifier": "8.2.8",
        "domain": DOMAIN_8,
        "description": "If a user session has been idle for more than 15 minutes, the user is required to re-authenticate to re-activate the terminal or session.",
        "guidance": "When users walk away from an open machine with access to system components or cardholder data, there is a risk that the machine may be used by others in the user's absence, resulting in unauthorized account access and/or misuse. Timed-out controls balance the risk of access through an unattended session against the need for legitimate use. However, timed-out controls balance the risk of access and the need for a user to access the system. If a user needs to run a program from an unattended computer, the user and purpose of the access should be documented and the access should be controlled.",
    },
    {
        "identifier": "8.3.1",
        "domain": DOMAIN_8,
        "description": "All user access to system components for users and administrators is authenticated via at least one of the following authentication factors: Something you know, such as a password or passphrase; Something you have, such as a token device or smart card; Something you are, such as a biometric element.",
        "guidance": "When used in addition to unique IDs, an authentication factor helps protect user IDs from being compromised, since the attacker needs to have the unique ID and compromise the associated authentication factor. A common approach for a malicious individual to compromise a system is to exploit weak or nonexistent authentication factors (for example, passwords/passphrases). Requiring strong authentication factors helps protect against these attacks.",
    },
    {
        "identifier": "8.3.2",
        "domain": DOMAIN_8,
        "description": "Strong cryptography is used to render all authentication factors unreadable during transmission and storage on all system components.",
        "guidance": "Network devices and applications have been known to transmit unencrypted, readable authentication factors (such as passwords and passphrases) across the network and/or store these values without encryption. As a result, a malicious individual can easily intercept this information during transmission using a sniffer, or directly access unencrypted authentication factors in files where they are stored, and then use this data to gain unauthorized access. Modifications to authentication factors for which the values are not displayed (such as passwords) should require re-validation of the new value to confirm it was entered correctly.",
    },
    {
        "identifier": "8.3.3",
        "domain": DOMAIN_8,
        "description": "User identity is verified before modifying any authentication factor.",
        "guidance": "Requiring positive identification of the user requesting a change to an authentication factor helps ensure that a change is not being made by a malicious individual impersonating a legitimate user. Modifications to authentication factors for which the values are not displayed, such as passwords, should require re-validation of the new value to confirm it was entered correctly. Help desk personnel should be limited to performing password resets, provisioning new hardware or software tokens, generating new enrollment links, or biometrics re-registration over known, previously established phone numbers.",
    },
    {
        "identifier": "8.3.4",
        "domain": DOMAIN_8,
        "description": "Invalid authentication attempts are limited by: Locking out the user ID after not more than 10 attempts; Setting the lockout duration to a minimum of 30 minutes or until the user's identity is confirmed.",
        "guidance": "Without account-lockout mechanisms in place, an attacker can continually try to guess a password through manual or automated tools (for example, password cracking), until the attacker succeeds and gains access to a user's account. If an account is locked out due to someone continually trying to guess a password, controls to delay reactivation of these locked accounts stop the malicious individual from continually guessing the password as they will have to stop for a minimum of 30 minutes until the account is reactivated.",
    },
    {
        "identifier": "8.3.5",
        "domain": DOMAIN_8,
        "description": "If passwords/passphrases are used as authentication factors to meet Requirement 8.3.1, they are set and reset for each user as follows: Set to a unique value for first-time use and upon reset; Forced to be changed immediately after the first use.",
        "guidance": "If the same password/passphrase is used for every new user, an internal user, former employee, or malicious individual may know or easily discover the value and use it to gain access to accounts before the authorized user attempts to use the password. Forcing a password/passphrase change immediately after the first time it is used ensures that once the new user has received that password, it is immediately replaced with a password that only that user knows.",
    },
    {
        "identifier": "8.3.6",
        "domain": DOMAIN_8,
        "description": "If passwords/passphrases are used as authentication factors to meet Requirement 8.3.1, they meet the following minimum level of complexity: A minimum length of 12 characters (or if the system does not support 12 characters, a minimum length of eight characters); Contain both numeric and alphabetic characters.",
        "guidance": "Strong passwords/passphrases may be the first line of defense into a network since a malicious individual often first tries to find accounts with weak, static, or non-existent passwords. If passwords are short or easily guessable, it is relatively easy for a malicious individual to find these weak accounts and compromise a network under the guise of a valid user ID. Requiring that passwords/passphrases have both a minimum complexity and length provides additional security against brute-force guessing attacks. Another option for increasing the resistance of passwords to guessing attacks is by comparing proposed passwords against a list of known bad, breached, or commonly used passwords and having users choose a new password for any that match. Additional complexity increases the time required for offline brute-force attacks.",
    },
    {
        "identifier": "8.3.7",
        "domain": DOMAIN_8,
        "description": "Individuals are not allowed to submit a new password/passphrase that is the same as any of the last four passwords/passphrases used.",
        "guidance": "If password history is not maintained, the effectiveness of changing passwords is reduced, as previous passwords can be reused over and over. Requiring that passwords cannot be reused for a period reduces the likelihood that passwords that have been guessed or brute-forced will be re-used in the future. Passwords or passphrases that they have previously used should not be re-used because the passwords or passphrases may already be compromised and there is an increased risk of their re-use, both of which are reasons why already-used passwords should not be reused.",
    },
    {
        "identifier": "8.3.8",
        "domain": DOMAIN_8,
        "description": "Authentication policies and procedures are documented and communicated to all users including: Guidance on selecting strong authentication factors; Guidance for how users should protect their authentication factors; Instructions not to reuse previously used passwords/passphrases; Instructions to change passwords/passphrases if there is any suspicion or knowledge that the password/passphrases have been compromised and how to report the incident.",
        "guidance": "Communicating authentication policies and procedures to all users helps them to understand and abide by the policies. Guidance for protecting authentication factors may include not writing down passwords or saving them in insecure files, and being alert for malicious individuals who may try to exploit their passwords. Guidance for selecting strong passwords may include suggestions to help personnel select difficult-to-guess passwords or passphrases that do not contain dictionary words, and information about the user ID, names of family members, date of birth, etc.",
    },
    {
        "identifier": "8.3.9",
        "domain": DOMAIN_8,
        "description": "If passwords/passphrases are used as the only authentication factor for user access (i.e., in any single-factor authentication implementation) then either: Passwords/passphrases are changed at least once every 90 days; OR The security posture of accounts is dynamically analyzed, and real-time access to resources is automatically determined accordingly.",
        "guidance": "Access to system components in the CDE may be provided using a single authentication factor, such as a password/passphrase, a token device or smart card, or a biometric. Where passwords/passphrases are employed as the only authentication factor for user access, additional controls are required to protect the integrity of the password/passphrase. Passwords/passphrases that are valid for a long time without a change provide malicious individuals with more time to break the password/passphrase. Periodically changing passwords/passphrases offers less time to a malicious individual to crack a password/passphrase and less time to use a compromised password/passphrase.",
    },
    {
        "identifier": "8.3.10",
        "domain": DOMAIN_8,
        "description": "Additional requirement for service providers: If passwords/passphrases are used as the only authentication factor for customer user access to cardholder data (i.e., in any single-factor authentication implementation), then guidance is provided to customer users including: Guidance for customers to change their user passwords/passphrases periodically; Guidance as to when, and under what circumstances, passwords/passphrases are to be changed.",
        "guidance": "Using a password/passphrase as the only authentication factor provides a single point of failure if compromised. Therefore, in these implementations, controls are needed to minimize how long malicious activity could occur via a compromised password/passphrase. Passwords/passphrases that are valid for a long time without a change provide malicious individuals with more time to break the password/passphrase. Periodically changing passwords/passphrases offers less time for a malicious individual to crack a password/passphrase and less time to use a compromised password/passphrase.",
    },
    {
        "identifier": "8.3.10.1",
        "domain": DOMAIN_8,
        "description": "Additional requirement for service providers: If passwords/passphrases are used as the only authentication factor for customer user access (i.e., in any single-factor authentication implementation) then either: Passwords/passphrases are changed at least once every 90 days; OR The security posture of accounts is dynamically analyzed, and real-time access to resources is automatically determined accordingly.",
        "guidance": "Using a password/passphrase as the only authentication factor provides a single point of failure if compromised. Therefore, in these implementations, controls are needed to minimize how long malicious activity could occur via a compromised password/passphrase. Dynamically analyzing the security posture of accounts and granting access in real time based on the analysis can help to detect and respond to suspicious behavior more rapidly. Domain detection and response helps entities detect anomalies or suspicious changes that could pose a risk. For example, takes a number of data points which may individually be low or medium risk, could collectively pose a higher risk whether an account can be granted access, and then whether that access should be limited or should be revoked. It can also detect and account lockout if it is suspected that account credentials have been compromised.",
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
