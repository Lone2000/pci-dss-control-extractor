import csv

OUTPUT = r"c:\Users\PC\Desktop\Control Outputs\PCI_Controls_Preview.csv"

DOMAIN_1 = "Requirement 1: Install and Maintain Network Security Controls"

controls = [
    {
        "identifier": "1.1.1",
        "domain": DOMAIN_1,
        "description": "All security policies and operational procedures that are identified in Requirement 1 are: Documented, Kept up to date, In use, Known to all affected parties.",
        "guidance": "Requirement 1.1.1 is about effectively managing and maintaining the various policies and procedures specified throughout Requirement 1. While it is important to define the specific policies or procedures called out in Requirement 1, it is equally important to ensure they are properly documented, maintained, and disseminated. It is important to update policies and procedures as needed to address changes in processes, technologies, and business objectives. For these reasons, consider updating these documents as soon as possible after a change occurs and not only on a periodic cycle.",
    },
    {
        "identifier": "1.1.2",
        "domain": DOMAIN_1,
        "description": "Roles and responsibilities for performing activities in Requirement 1 are documented, assigned, and understood.",
        "guidance": "If roles and responsibilities are not formally assigned, personnel may not be aware of their day-to-day responsibilities and critical activities may not occur. Roles and responsibilities may be documented within policies and procedures or maintained within separate documents. As part of communicating roles and responsibilities, entities can consider having personnel acknowledge their acceptance and understanding of their assigned roles and responsibilities.",
    },
    {
        "identifier": "1.2.1",
        "domain": DOMAIN_1,
        "description": "Configuration standards for NSC rulesets are: Defined, Implemented, Maintained.",
        "guidance": "The implementation of these configuration standards results in the NSC being configured and managed to properly perform their securityfunction (often referred to as the ruleset). These standards often define the requirements for acceptable protocols, ports that are permitted tobe used, and specific configuration requirements that are acceptable. Configuration standards may also outline what the entity considers not acceptable or not permitted within its network.",
    },
    {
        "identifier": "1.2.2",
        "domain": DOMAIN_1,
        "description": "All changes to network connections and to configurations of NSCs are: Approved and managed in accordance with the change control process defined at Requirement 6.5.1.",
        "guidance": "A structured change control process for all changes to NSCs reduces the risk that a change could introduce a security vulnerability. Changes should be approved by individuals with the appropriate authority and knowledge to understand the security impact of the change, and should provide reasonable assurance that the change will not impact the existing or required security of the NSC. Changes should not be implemented by individuals responsible for managing the network connections. All changes should be reviewed and verified prior to being implemented and verified to be approved by a qualified individual. In addition to confirming the change itself, network documentation and diagrams should be updated to reflect the change and the actual configuration.",
    },
    {
        "identifier": "1.2.3",
        "domain": DOMAIN_1,
        "description": "An accurate network diagram(s) is maintained that shows all connections between the trusted and untrusted networks and any wireless networks.",
        "guidance": "An accurate and up-to-date network diagram prevents network connections and devices from being overlooked and unknowingly excluded from the security controls implemented for PCI DSS. A properly maintained network diagram helps the organization verify its PCI DSS scope and serves as a reference for clarifying the boundaries of the CDE. Entities should consider including the following in their network diagrams: all connections to and from the CDE regardless of whether the systems providing security-related services are in-scope system components; cardholder data flows, wireless networks, cloud providers; all sources of all network segments; all security services providing functionality including unique locations for each control; and all in-scope system components including firewalls, routers, wireless access points, load balancers, IDS/IPS, log aggregation systems, payment applications, and payment terminals. Clear labeling of any out-of-scope areas, date of last update, names of people that last updated the diagram, and a legend or key to explain the diagram should be included. Diagrams should be updated by authorized personnel and approved by management to provide an accurate description of the network.",
    },
    {
        "identifier": "1.2.4",
        "domain": DOMAIN_1,
        "description": "An accurate data-flow diagram(s) is maintained that meets the following: Shows all account data flows across systems and networks.",
        "guidance": "An up-to-date, readily available data-flow diagram helps an organization understand and keep track of the scope of its environment by documenting account data flows across networks and between individual systems and devices. This helps to prevent account data from being overlooked and allows undiscovered data flows to be identified. The data-flow diagram should include all connection points where account data is received from or sent to other entities, including connections to open, public networks, application processing flows, storage, and transmissions between systems. The data-flow diagram is meant to be in addition to and augment the network diagram. As a best practice, entities should consider including in their data-flow diagrams: all distinct acceptance channels including e-commerce, card-not-present, and e-channels; all types of data receipt or transmission; the flow of account data from the point where data enters the environment to its final disposition; where account data is transmitted and processed; the sources of all account data received and outgoing transmissions and destinations; and date of last update and names of people that made and approved the updates.",
    },
    {
        "identifier": "1.2.5",
        "domain": DOMAIN_1,
        "description": "All services, protocols, and ports allowed are: Documented, Approved, and have a defined business need.",
        "guidance": "Compromises often happen due to unused or insecure services (for example, telnet and FTP), protocols, and ports, since these can lead to unnecessary points of entry into the CDE. Additionally, services, protocols, and ports that are not needed can lead to compromised and undetected vulnerabilities. By identifying the services, protocols, and ports that each NSC must use, the entity can ensure that any services, protocols, and ports not on that list are not permitted into or out of the network. The security risk associated with each service, protocol, and port allowed should be understood. Approving management should be aware of the business need and understand the risk involved with each service, protocol, and port, and each should have an explicit approval documented. Approving management should be independent of those managing the configuration.",
    },
    {
        "identifier": "1.2.6",
        "domain": DOMAIN_1,
        "description": "Security features are defined and implemented for all services, protocols, and ports that are in use and considered to be insecure, such that the risk is mitigated.",
        "guidance": "If insecure services, protocols, or ports are in use, they can take advantage of insecure network configurations. The security features associated with each service, protocol, or port should be directly linked to the relevant entity's risk assessment for that service, protocol, or port. If insecure services, protocols, or ports are necessary for business, the risk of using these services, protocols, or ports should be clearly understood and accepted by the organization, and security features should be defined and implemented by the entity to mitigate the risk of using these services, protocols, or ports. For guidance on services, protocols, or ports considered to be insecure, refer to industry standards and guidance (for example, from NIST, ENISA, OWASP).",
    },
    {
        "identifier": "1.2.7",
        "domain": DOMAIN_1,
        "description": "Configurations of NSCs are reviewed at least once every six months to confirm they are relevant and effective.",
        "guidance": "This requirement gives the organization an opportunity to clean up any unneeded, outdated, or incorrect rules and configurations which could be used by malicious personnel. Furthermore, it ensures that all rules and configurations are current and aligned with current processes, technologies, and business objectives. The review can be implemented using manual, automated, or system-based methods. While this requirement specifies that this review should occur at least once every six months, organizations may wish to consider performing reviews more frequently to ensure that their network configurations remain in accordance with policy and business justifications. Any discrepancies or uncertainties about a rule or configuration should be resolved by consulting the change documentation and comparing the change documentation against the actual configuration.",
    },
    {
        "identifier": "1.2.8",
        "domain": DOMAIN_1,
        "description": "Configuration files for NSCs are: Secured from unauthorized access, Kept consistent with active network configurations.",
        "guidance": "Keeping the configuration information current and secured prevents unauthorized changes from being applied to the network, as stored files with configurations for network controls need to be kept consistent with active network configuration changes. Keeping configuration files secured from unauthorized access ensures the correct configuration is applied whenever the configuration is initialized. Configuration information for a router stored in non-volatile memory, when that router is restarted or rebooted, these controls should ensure that its secure configuration is applied whenever the configuration is initialized.",
    },
    {
        "identifier": "1.3.1",
        "domain": DOMAIN_1,
        "description": "Inbound traffic to the CDE is restricted as follows: To only traffic that is necessary; All other traffic is specifically denied.",
        "guidance": "This requirement aims to prevent malicious individuals and compromised system components within the entity's network from communicating with external untrusted systems via unauthorized IP addresses or from using insecure services, protocols, or ports in an unauthorized direction. All traffic inbound to the CDE, regardless of where it comes from, should be evaluated. Implementing a rule that denies all inbound and outbound traffic that is not specifically needed—an implicit deny after allow statement—helps to prevent inadvertent misconfiguration that may allow traffic from untrusted networks to access the CDE. Implementing a rule that restricts source/destination addresses and ports to prevent potentially harmful traffic from entering or exiting the CDE.",
    },
    {
        "identifier": "1.3.2",
        "domain": DOMAIN_1,
        "description": "Outbound traffic from the CDE is restricted as follows: To only traffic that is necessary; All other traffic is specifically denied.",
        "guidance": "This requirement aims to prevent malicious individuals and compromised system components within the entity's network from communicating with external untrusted systems via unauthorized IP addresses or from using insecure services, protocols, or ports in an unauthorized direction. All traffic outbound from the CDE, regardless of where it is going, should be evaluated. Implementing a rule that denies all outbound traffic that is not specifically needed allows for the identification of traffic that is specifically needed and allows for its explicit allowance. An implicit deny after allow statement helps to prevent inadvertent misconfiguration that may allow traffic from the CDE to reach untrusted networks by restricting source/destination addresses and ports to prevent potentially harmful traffic.",
    },
]

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Control ID", "Control", "Control Description", "Criticality",
        "Domain", "Framework (FK)", "Identifier", "Implementation Guidance",
        "Is Active", "Mapped Controls", "Type", "Weight"
    ])
    for i, c in enumerate(controls, start=1):
        writer.writerow([
            i, "", c["description"], "", c["domain"],
            7, c["identifier"], c["guidance"],
            "Yes", "", "", ""
        ])

print(f"Written {len(controls)} rows to {OUTPUT}")
