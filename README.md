# DarkOps

DarkOps is an IRM (Internal Risk Management), SaaS application, and what I'd like to call an **ITDM&R (Insider Threat Detection, Management & Response)** platform designed to act as a security layer for applications, websites and other digital services.

🌑 Permanent dark theme
🟠 Foldit as one of the primary/entire UI typeface
🟠 Bronze/orange borders and accents
⚫ Near-black surfaces

It is intended to align with the **NIST Cybersecurity Framework (CSF) 2.0** and relevant **CISA** incident-response practices.

*DarkOps does the security work quietly and brings the user back only when they need to act.*

## Core Purpose

DarkOps does not need to own a company's sensitive business data. Instead, it manages the **security state and security events of systems registered with it**.

Its long-term goal is to provide a reusable cybersecurity service that can be integrated into platforms such as **KLuv AI** or other authorized applications.

*DarkOps should never win a customer by claiming to be bigger than every other cybersecurity platform. It should win by being specific about what it protects, what it actually does, what it intentionally does not do, and by proving that it works.*

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

Future files/functions needed:
vault/api/security/
    detection.py
    policy.py
    posture.py
    console.py
    permissions.py
    authorization.py
    response.py
    recovery.py

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
```

*I'd trust DarkOps because of what it refuses to do, how transparent it is, and what it can demonstrate.*

## Additional functions for DarkOps

3 foreign APIs are to boost DarkOps functionality, but what makes DarkOps unique from other services like CrowdStrike, Microsoft Pursuit, Proofpoint ITM, CyberHaven and DTEX Systems? That's the DarkOps DNA! As I continue improving this in Rust in the near future, here are the features it will have in store for any organization (for cheap):

```Python tools for DarkOps
| Module | Core Python Library | Core Rust Crate | Zero-API Mechanism |
| :--- | :--- | :--- | :--- |
| **DLP** | `watchdog` + `re` | `notify` + `regex` | OS-native event hooks (`inotify`/`ReadDirectoryChangesW`) for zero-latency file scanning |
| **Credential Vaulting** | `cryptography.fernet` | `ring` / `aes-gcm` / `fernet` | Bare-metal AES-256-GCM / HMAC encryption with thread-safe ephemeral memory buffers |
| **Process Lineage** | `psutil` | `sysinfo` / `procfs` | Inspecting process trees directly via system kernel memory with zero runtime overhead |
| **Immutable Logging** | `hashlib` | `sha2` | High-speed SHA-256 block-linked hash chains written directly to binary audit logs |
| **Automated Containment** | `psutil` + `os` | `nix` / `windows-sys` | Native OS syscalls (`kill`, `ptrace`, `TerminateProcess`) for sub-millisecond process intervention |
```

---

## Fonts and primary palettes

1. Primary 1 — Charcoal (#1A1A1A)

2. Primary 2 — Burnt Orange (#C65A24)

3. Optional third — Warm Grey (#8A8580)

- Foldit → ONLY large titles/subtitles.
- Inter → normal UI, body, tables, metadata, numbers, graphs, axes, etc.
- Gabriela → occasional decorative notification/event treatment.

***This is just a part of DarkOps, NOT DarkOps' whole identity. It takes more than that.*** ✓✗

---

## Duo Dev API Service

```Diagram for DarkOps
                 DARKOPS
                    │
             DUO DEV API
              /          \
             /            \
      BUILD MODE       PROTECTION MODE
          │                  │
          ↓                  ↓
   Use DarkOps        Let DarkOps protect
   capabilities       your application
          │                  │
          ↓                  ↓
   Developer builds      DarkOps operates
   their own product     behind the scenes
```

1. Duo Dev Build
90 days
API requests / capabilities

2. Duo Dev Protection
90 days
Protected application / telemetry allowance

3. DarkOps Console
90 days
Managed application protection

***A large company is still a collection of users operating through a "Team"***

## Credit Expenditure Measurement

These consist of Workload and Duo Dev credits:

**Workload Credits** -- These are the credits assigned to registered users per day for protection services for applications, whether device apps or web apps (with links provided for web apps).

**Duo Dev API Credits** -- these are the credits spent when a user/team accesses the provided API Keys and are valid/permitted to expose/manage DarkOps' capabilities.

```Workload Table
| Workload                                                  |       V1 credits |
| --------------------------------------------------------- | ---------------: |
| Protected application processing cycle — 1 app / 1 minute |           **10** |
| Transient event evaluated and discarded                   | **0 additional** |
| Security-relevant event retained                          |            **5** |
| Low/informational alert                                   |           **15** |
| Medium alert                                              |           **20** |
| High alert                                                |           **25** |
| Critical alert                                            |           **30** |
| Internal asset/context analysis                           |           **25** |
| Security document/file metadata analysis                  |           **20** |
| Traceback/security-log analysis                           |           **25** |
| HTTPS/TLS analysis                                        |           **10** |
| IPInfo lookup                                             |           **15** |
| REST Countries lookup                                     |            **5** |
| HIBP email/domain lookup                                  |           **30** |
| Threat/context correlation                                |           **25** |
| Vulnerability assessment                                  |           **40** |
| Incident creation                                         |           **50** |
| Incident action                                           |           **10** |
| Incident note                                             |            **5** |
| Audit record persistence                                  |            **2** |
| In-app notification record                                |            **1** |
| Email delivery                                            |            **3** |
| Webhook delivery                                          |            **5** |
| SMS delivery                                              |            **8** |
| WebSocket/chat                                            |            **0** |
| Sonner/toast rendering                                    |            **0** |

```

In-app notification record = 1 Workload credit

---

The "Maximum Enrichment Bundle is important because it isn't plainly one service costing most credits;

```MEB Summary
25  internal asset analysis
20  security document metadata analysis
25  traceback/log analysis
10  HTTPS/TLS analysis
15  IP intelligence
 5  country intelligence
30  HIBP
25  correlation
───
155 credits maximum
```

---

```Duo Dev Credit table
| Duo Dev API operation                            | Credits |
| ------------------------------------------------ | ------: |
| `GET`                                            |   **1** |
| `POST`                                           |   **2** |
| `PATCH`                                          |   **2** |
| `DELETE` / revoke                                |   **2** |
| Bulk event submission                            |   **5** |
| Webhook registration/update                      |   **2** |
| Build capability invocation — lightweight        |   **5** |
| Build capability invocation — security operation |  **10** |
| Protection telemetry submission                  |   **2** |
| Protection security-operation request            |   **5** |
| API key creation/rotation                        |   **5** |
| API health/status request                        |   **1** |
```

We want to be transparent about how pricing is measured; not by member count, but by security workload.

***Inspect the environment, not the user's secrets***

---
