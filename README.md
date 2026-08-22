# DarkOps

DarkOps is an **ITDM&R (Insider Threat Detection, Management & Response)** platform designed to act as a security layer for applications, websites, devices, and services.

🌑 Permanent dark theme
🟠 Foldit as the primary/entire UI typeface
🟠 Bronze/orange borders and accents
⚫ Near-black surfaces

It is intended to align with the **NIST Cybersecurity Framework (CSF) 2.0** and relevant **CISA** incident-response practices.

## Core Purpose

DarkOps does not need to own a company's sensitive business data. Instead, it manages the **security state and security events of systems registered with it**.

Its long-term goal is to provide a reusable cybersecurity service that can be integrated into platforms such as **KLuv AI** or other authorized applications.

---

## NIST-Aligned Security Model

DarkOps follows the six NIST CSF 2.0 Functions:

1. **Govern** — policies, roles, permissions, configurations and auditing.
2. **Identify** — applications, devices, APIs, domains, users and other assets.
3. **Protect** — security controls, access management and defensive configuration.
4. **Detect** — suspicious activity, anomalies, vulnerabilities and threat intelligence.
5. **Respond** — investigate, assign, contain and manage security incidents.
6. **Recover** — resolve incidents, review outcomes and improve security posture.

---

## Core Data

DarkOps should manage structured security information such as:

- Organizations
- Applications and services
- Devices and assets
- Users and roles
- Security events
- Alerts
- Incidents
- Vulnerability findings
- Threat indicators
- Threat intelligence
- Response actions
- Audit logs
- Security posture information

DarkOps should **not** become the primary authentication/password database for connected applications.

---

## Incident Lifecycle

A basic incident can follow:

```text
Detected
   ↓
Investigating
   ↓
Contained
   ↓
Resolved
   ↓
Reviewed

                    DarkOps
                       │
        ┌──────────────┴──────────────┐
        │                             │
    Frontend                       Backend
        │                             │
 Dashboard / Assets            REST API
 Alerts / Incidents            PostgreSQL
 Intelligence                  Event Processing
 Users / Settings              Incident Engine
                                Audit Logging
                                      │
                         External Intelligence APIs
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                      KLuv AI              Other Applications
