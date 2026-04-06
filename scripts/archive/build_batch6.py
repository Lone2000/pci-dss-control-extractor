import csv
import os

OUTPUT = r"c:\Users\PC\Desktop\Control Outputs\PCI_Controls_Preview.csv"
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
    {
        "identifier": "10.4.1",
        "domain": DOMAIN_10,
        "description": "The following audit logs are reviewed at least once daily: All security events. Logs of all system components that store, process, or transmit CHD and/or SAD. Logs of all critical system components. Logs of all servers and system components that perform security functions (for example, network security controls, intrusion-detection systems/intrusion-prevention systems (IDS/IPS), authentication servers, e-commerce redirection servers, etc.).",
        "guidance": "Checking logs daily (7 days a week, 365 days a year, including holidays) minimizes the amount of time and exposure of a potential breach. Log harvesting, parsing, and alerting tools, centralized log management systems, event log analyzers, and security information and event management (SIEM) solutions are examples of automated tools that can be used to meet this requirement. Daily review of security events—for example, notifications or alerts that identify suspicious or anomalous activities—as well as logs from critical system components, and logs from systems that perform security functions, such as firewalls, IDS/IPS, file integrity monitoring (FIM) systems, etc., is necessary to identify potential issues. The determination of \"security event\" will vary for each organization and may include consideration for the type of technology, location, and function of the device. Organizations may also wish to maintain a baseline of \"normal\" traffic to help identify anomalous behavior. An entity that uses third-party service providers to perform log review services should ensure that a context is provided to the service provider, so it understands the entity's environment, policies, and procedures and can establish a baseline of \"normal\" traffic to help identify anomalous behavior, and can alert about anomalous events and provide information and context about the entity's environment.",
    },
    {
        "identifier": "10.4.1.1",
        "domain": DOMAIN_10,
        "description": "Automated mechanisms are used to perform audit log reviews.",
        "guidance": "Manual log reviews are difficult to perform, even for one or two systems, due to the amount of log data that is generated. However, using log harvesting, parsing, and alerting tools, centralized log management systems, event log analyzers, and security information and event management (SIEM) solutions can help facilitate the process by identifying log events that need to be reviewed. Establishing a baseline of normal audit activity patterns is critical to the effectiveness of an automated review. Each entity should keep logging tools aligned with any changes in the established baselines, and should update any changes in its environment to reflect any change occurring in the established baselines. The entity should also keep logging tools updated to reflect any changes and updates. Effective log management solutions collect and format log data from disparate sources to facilitate analysis.",
    },
    {
        "identifier": "10.4.2",
        "domain": DOMAIN_10,
        "description": "Logs of all other system components (those not specified in Requirement 10.4.1) are reviewed periodically.",
        "guidance": "Periodic review of logs for all other system components (not specified in Requirement 10.4.1) helps to identify indications of potential issues or attempts to access critical systems via less-critical systems.",
    },
    {
        "identifier": "10.4.2.1",
        "domain": DOMAIN_10,
        "description": "The frequency of periodic log reviews for all other system components (not defined in Requirement 10.4.1) is defined in the entity's targeted risk analysis, which is performed according to all elements specified in Requirement 12.3.1.",
        "guidance": "Entities can determine the optimum period to review these logs based on criteria such as the complexity of each entity's environment, the number of types of systems that are required to be evaluated, and the functions of such systems.",
    },
    {
        "identifier": "10.4.3",
        "domain": DOMAIN_10,
        "description": "Exceptions and anomalies identified during the review process are addressed.",
        "guidance": "If exceptions and anomalies identified during the log-review process are not investigated, the entity may be unaware of unauthorized and potentially malicious activities occurring within their network. Entities should consider how to address the following when defining and managing exceptions and anomalies: How to mark and prioritize exceptions and anomalies; How to escalate and report exceptions and anomalies, and escalable exceptions and anomalies, and procedures for escalation; Who is responsible for investigating and for any remediation tasks.",
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
