# DARKOPS — PRODUCT TRUTH

This should become the foundation for the README, website, onboarding, pricing, product UI, sales material, and eventually even the way we design the API. A security product needs a very clear answer to: *What problem are we solving, for whom, and why should anyone trust us with part of their security?*

**There is no reason to burn time implementing hundreds of endpoints before we are certain the product deserves those endpoints.**

---

## 1. What DarkOps actually IS

The cleanest definition is:

> **DarkOps is an application-centric security platform that continuously monitors the security state of applications and their authorized internal access, detects meaningful security risks, and gives the people responsible for those applications a structured way to investigate, respond, and maintain an auditable security record.**

The phrase **application-centric** is extremely important.

DarkOps isn't trying to become:

> "We monitor everything happening everywhere in your company."

That's already a huge category occupied by SIEM, XDR, EDR, identity-security, cloud-security and insider-risk platforms.

DarkOps begins with something much narrower:

```text
                 YOUR APPLICATION
                       │
         ┌─────────────┼─────────────┐
         ↓             ↓             ↓
       Assets        Events        Access
         │             │             │
         └─────────────┼─────────────┘
                       ↓
                    DARKOPS
                       ↓
             Security understanding
                       ↓
            ┌──────────┼───────────┐
            ↓          ↓           ↓
          Alerts    Incidents   Response
            │          │           │
            └──────────┼───────────┘
                       ↓
                  Audit history
```

The customer's business data is **not the product's central object**.

The central object is the **security state of an authorized application/system**.

That distinction gives DarkOps an actual identity.

---

## 2. What does "insider" mean here?

This is another place where we need to be precise.

CISA defines an insider broadly as somebody who has or had authorized access to an organization's resources, including employees, contractors, vendors and others with authorized access.

So DarkOps can legitimately use the term **insider threat** without meaning:

> "Your employees are criminals."

An insider-related security event could be:

```text
Employee accidentally exposes something
              ↓
Contractor uses an unexpected privilege
              ↓
Compromised employee account performs unusual action
              ↓
Administrator makes a dangerous configuration change
              ↓
Authorized user interacts with an application unexpectedly
```

The system therefore shouldn't start by assuming malicious intent.

It asks:

> **"Was this authorized behavior consistent with the security expectations of this application?"**

That is a much healthier foundation for the product.

---

## 3. What DarkOps is CAPABLE of

This is where we need to separate **what DarkOps actually intends to provide** from what sounds impressive on a cybersecurity website.

### Govern

DarkOps can provide the organizational control layer:

```text
Users
Teams
Roles
Permissions
Applications
API keys
Subscriptions
Security configuration
Audit records
```

NIST CSF 2.0 explicitly added **Govern** as a sixth function alongside Identify, Protect, Detect, Respond and Recover.

DarkOps can use that structure as an organizing principle without claiming to *be* NIST.

### Identify

DarkOps establishes:

```text
Application
    ↓
Assets
    ↓
Security events
    ↓
Vulnerabilities
    ↓
Security context
```

An asset might be:

```text
HTTPS URL
Backend endpoint
IP address
Domain
Email address
Device application
Security-related reference
```

The point is to establish **what DarkOps is protecting and what security information belongs to it**.

### Protect

Protection in DarkOps is not necessarily:

> "Install our enormous agent everywhere."

The V1 direction is much more controlled.

Applications deliberately connect to DarkOps and provide authorized security information through supported mechanisms.

For example:

```text
Customer application
       │
       │ authorized API
       ↓
     DarkOps
```

And device applications can use the V1 Android/Windows clients where appropriate.

### Detect

This is where DarkOps earns its name.

DarkOps can receive security events, associate them with applications/assets, evaluate severity and context, correlate information, enrich it with external intelligence, and produce alerts.

The current intelligence integrations are particularly useful here:

```text
HIBP
IPInfo
REST Countries
       ↓
DarkOps
       ↓
Security context
```

Those external systems remain **inputs**, not the actual security platform.

### Respond

A detection shouldn't simply become a red notification that somebody ignores.

DarkOps has the structure for:

```text
Alert
   ↓
Investigation
   ↓
Incident
   ↓
Incident notes
   ↓
Incident actions
   ↓
Resolution
```

### Recover

The system retains the incident history, actions, resolution and audit trail so the business can understand what happened afterward.

That lines up naturally with the lifecycle represented by NIST CSF 2.0.

---

## 4. The most important DarkOps experience

Here's something I think should become a **core product promise**, rather than just a UI preference:

> **Connect it. Configure it. Let it work. Come back when something matters.**

That is powerful.

A security platform shouldn't make the customer feel like they bought another full-time job.

DarkOps should therefore be designed around:

```text
NORMAL STATE

Application connected
       ↓
DarkOps continuously evaluates
       ↓
Nothing important
       ↓
Customer does nothing


IMPORTANT EVENT

Application
    ↓
Security event
    ↓
DarkOps analysis
    ↓
Alert
    ↓
Notification
    ↓
Customer investigates
```

That's a very different experience from:

> "Log into our security dashboard every morning and manually inspect 74 charts."

---

## 5. Who DarkOps is FOR

I would define the initial customer around the **application**, not the company's industry.

### Primary customer

Businesses that operate applications they are responsible for securing:

```text
SaaS companies
Software companies
Web businesses
Digital platforms
Application-dependent SMEs
Technology departments
Internal software teams
Organizations running custom business applications
```

The common characteristic isn't:

> "They are a financial company."

It's:

> **"Their business depends on digital applications and they need to know when something security-relevant happens inside those applications or their authorized operating environment."**

That's much more scalable.

### Secondary customer

Development teams and organizations that want their own applications to interact with DarkOps programmatically.

That's where **Duo Dev** matters.

```text
Customer application
       │
       ├── Build Mode
       │
       └── Protection Mode
                ↓
             DarkOps
```

Build Mode means:

> "Use DarkOps security capabilities as part of another application."

Protection Mode means:

> "Have DarkOps provide security functionality behind our application."

Those are fundamentally different use cases, and we've already reflected that distinction in the API-key design.

### Individual/developer customer

The free individual tier gives DarkOps somewhere to start:

```text
Developer
Solo builder
Independent operator
Small application owner
```

That matters because a security platform should not require someone to already be a giant corporation before they can understand what it does.

---

## 6. Who DarkOps is NOT FOR

This is equally important.

DarkOps V1 should **not** pretend to replace every cybersecurity product.

It is not currently:

```text
A full EDR
A full XDR
A general-purpose SIEM
A WAF
An IAM platform
A complete DLP platform
A cloud-security platform
A vulnerability scanner for every piece of infrastructure
An employee surveillance system
A SOC outsourcing service
```

That honesty is actually part of the product's credibility.

For example, Microsoft Purview Insider Risk Management correlates user/activity signals to identify potentially malicious or inadvertent insider risks and includes policy controls, pseudonymization and auditing.

That's a legitimate security category.

But DarkOps isn't trying to reproduce Microsoft Purview.

Similarly, Wazuh provides XDR/SIEM functionality across endpoints and cloud workloads through agents and centralized components.

Splunk Enterprise Security combines SIEM, SOAR and threat-intelligence capabilities for security operations.

And platforms such as Snyk concentrate strongly on developer/application security across code, dependencies, containers and cloud infrastructure.

Palo Alto's Prisma Cloud/Cortex Cloud direction similarly spans application security from code through infrastructure and runtime.

Wiz is positioned around cloud and AI security, connecting code, cloud and runtime with broad cloud-resource visibility and attack-path analysis.

**That isn't competition we need to pretend doesn't exist.**

It tells us where DarkOps sits.

---

## 7. So what makes DarkOps different?

This is where we need to be careful.

I would **not** currently write:

> "DarkOps is the world's first..."

or:

> "Nobody else does this."

We don't have evidence for that.

Instead, the defensible differentiation is the **combination and boundary** we're choosing.

## DarkOps is deliberately application-centric

Rather than starting from:

```text
Every endpoint
Every employee
Every cloud resource
Every log
Every network
Every identity
Every application
```

DarkOps starts from:

```text
THIS APPLICATION
       ↓
Its authorized security state
       ↓
Its assets
       ↓
Its events
       ↓
Its incidents
```

That's a much smaller mental model.

And that can make the product easier to deploy and operate.

---

## 8. DarkOps versus major security categories

| Security category    | Typical center of gravity                                  | DarkOps' intended boundary                                                                                   |
| -------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| EDR/XDR              | Devices, endpoints, workloads, broad threat detection      | Application security state and authorized application activity                                               |
| SIEM/SecOps          | Large-scale collection, correlation, investigation         | Application-focused security monitoring and incident lifecycle                                               |
| Cloud security/CNAPP | Cloud infrastructure, identities, workloads, configuration | The application being protected, regardless of needing a huge cloud-security estate                          |
| Developer/AppSec     | Code, dependencies, CI/CD, IaC                             | Runtime/application security state and security operations                                                   |
| Insider Risk         | Users, behavior, data movement, organizational risk        | Internal/trusted access relationships **as they affect authorized applications**                             |
| DLP                  | Sensitive-data discovery/prevention                        | Not a V1 DarkOps capability                                                                                  |
| IAM                  | Authentication and authorization                           | DarkOps records/security context around authorized access; it isn't the customer's primary identity provider |

That last distinction is important.

DarkOps shouldn't become the company's replacement identity provider merely because access is relevant to security.

---

## 9. The biggest potential business benefit

This is where we need to be ruthless about the word **ROI**.

We cannot honestly promise:

> **"DarkOps guarantees your business will make money."**

No cybersecurity vendor can responsibly guarantee that.

What DarkOps **can** do is make the economic value measurable.

The ROI equation could eventually be:

```text
Security ROI
=
Labor saved
+
Security tooling costs avoided
+
Incident impact avoided
+
Downtime reduced
+
Investigation time reduced
+
Response efficiency gained
-
DarkOps cost
```

The **"incident impact avoided"** part is inherently an estimate. That's why we shouldn't market it as guaranteed savings.

But the first several components can be measured directly.

---

## 10. What a customer can actually measure

This is where DarkOps becomes commercially serious.

Before deployment:

```text
Average investigation time: 3 hours
Security tools involved: 5
Manual security checks: 40/week
Mean time to detect: 45 minutes
Mean time to investigate: 2 hours
Mean time to respond: 4 hours
```

After deployment:

```text
Security checks automated
↓
Events centralized
↓
Alerts contextualized
↓
Incidents structured
↓
Response activity recorded
```

Then the customer can measure:

### Time saved

How many hours did security/IT staff previously spend manually collecting and correlating application security information?

### Faster detection

How much time exists between a security event occurring and the responsible team becoming aware of it?

### Faster investigation

How long does an analyst spend figuring out:

```text
What happened?
Which application?
Which asset?
When?
What was affected?
What action was taken?
```

### Reduced tool switching

How many systems does someone currently need to check before understanding one application-security incident?

### Security coverage

How many applications are actually connected and producing meaningful security visibility?

### Response accountability

Can the organization show:

```text
Alert
 ↓
Investigator
 ↓
Action
 ↓
Timestamp
 ↓
Resolution
```

rather than relying on Slack messages, emails and someone's memory?

That's measurable business value.

---

## 11. There's an even bigger economic argument

Security doesn't only cost money when an incident happens.

It costs money **while people are trying to prevent incidents**.

A business may pay for:

```text
Monitoring tools
SIEM
Log storage
Threat intelligence
Incident-management tools
Security analysts
Developer security tooling
Third-party security services
Manual investigations
```

DarkOps can potentially create value by consolidating a **specific application-security workflow**, rather than claiming it replaces the whole cybersecurity stack.

That's a much more credible commercial argument.

And the reason the problem matters is not theoretical: Verizon's 2025 DBIR analyzed more than 22,000 incidents and 12,195 confirmed breaches; it reported credential abuse at 22% and vulnerability exploitation at 20% of breaches, while third-party involvement reached 30%.

IBM's 2025 breach-cost research reported a global average breach cost of **$4.44 million**, while also attributing savings to faster identification and containment.

That doesn't mean:

> "DarkOps will save your company $4.44 million."

Absolutely not.

It means **there is a quantifiable economic problem around security detection and response**, and DarkOps needs to prove its contribution to reducing that problem.

---

## 12. What would make ME trust DarkOps as a customer?

This is probably the most important section of everything you said.

Not:

> "We use AI."

Not:

> "Military-grade encryption."

Not:

> "Next-generation cybersecurity."

Those phrases mean almost nothing without evidence.

I'd trust DarkOps because of **what it refuses to do**, how transparent it is, and what it can demonstrate.

## 1. Explicit authorization

The customer explicitly tells DarkOps which application it is allowed to protect.

```text
Customer
   ↓
Register application
   ↓
Connect application
   ↓
Define authorized security assets
   ↓
DarkOps operates inside that boundary
```

That is much easier to understand than an opaque security product quietly ingesting half the organization.

## 2. Minimal data collection

DarkOps' philosophy should remain:

> **Inspect the security state, not the customer's business secrets.**

That's a strong trust principle.

The platform should collect what is necessary for security analysis rather than treating every available piece of customer information as fair game.

## 3. API keys are scoped

Duo Dev shouldn't be:

> "Here's one master key. Have fun."

The architecture already gives us:

```text
Build
Protection

Test
Live

Scopes
```

And team keys have an additional approval mechanism.

That's meaningful security design.

## 4. Everything important is auditable

A customer should be able to answer:

```text
Who did this?
What did they do?
When?
Through console or API?
Which application?
Which key?
Which incident?
```

That's why our AuditLog isn't just decoration.

## 5. Secret handling is deliberate

A generated API secret is shown once and then represented by its hash/prefix.

That matters enormously for customer trust.

## 6. Security boundaries are visible

The customer should always know:

```text
What applications are protected?
What assets are registered?
What integrations are enabled?
What API keys exist?
Which people have access?
What events were received?
What actions occurred?
```

No black box.

## 7. We show failures

This is underrated.

A trustworthy DarkOps shouldn't say:

> "Everything is secure."

It should say:

> "We detected this vulnerability."
> "This integration failed."
> "This asset hasn't reported recently."
> "This alert could not be enriched."

Security software that hides uncertainty is dangerous.

---

## 13. The DarkOps customer trust test

Eventually, I want a prospective customer to be able to ask these questions and DarkOps to answer every one:

```text
What exactly do you monitor?

Which applications can you access?

What data leave my application?

Where is my data stored?

How is API access authenticated?

How are API secrets stored?

Who can see my security information?

Can DarkOps access employee passwords?

Can DarkOps execute commands on my machines?

Can DarkOps change my application?

What happens when DarkOps detects a threat?

How are incidents recorded?

How do I remove my application?

How do I delete my data?

How do you handle outages?

How do you prove your security controls work?
```

And the answer shouldn't be hidden behind marketing language.

That's how we eventually build the **Trust Center**.

---

## 14. The business shouldn't have to "believe" DarkOps

This is the philosophical center I would use.

**Trust should come from evidence.**

Eventually:

```text
Documentation
       +
Security architecture
       +
Auditability
       +
Transparent limitations
       +
Penetration testing
       +
Dependency/security scanning
       +
Infrastructure controls
       +
Incident procedures
       +
Availability history
       +
Independent assessments
       ↓
      TRUST
```

We don't have all of those today.

And that's fine.

We're building toward them.

But we should **never pretend we already have certifications, independent audits, penetration-test results, uptime records, or compliance attestations that haven't happened.**

That's one of the easiest ways for a security startup to destroy its own credibility.

---

## 15. What DarkOps should promise

I think this is the strongest commercial promise:

> **DarkOps gives businesses a focused security layer around the applications they are responsible for, continuously turning security activity into actionable alerts, structured incidents, response records, and audit evidence—without requiring the business to surrender all of its underlying business data to the security platform.**

And underneath it:

> **Connect the application. Define what matters. DarkOps watches the security state.**

That's much stronger than trying to sell:

> "We do cybersecurity."

Because **everyone** says that.

---

## 16. What DarkOps should NOT promise

We should explicitly avoid:

```text
"Zero breaches guaranteed."
"Complete protection."
"100% threat detection."
"Your business can stop using every other security product."
"AI catches everything."
"DarkOps guarantees ROI."
"DarkOps makes you compliant."
```

Instead:

```text
"Designed to reduce security-monitoring workload."

"Designed to improve visibility into application security events."

"Designed to shorten detection and investigation workflows."

"Provides structured incident and audit records."

"Measures usage so customers can understand the security workload they are receiving."

"Supports security-risk management; it does not guarantee the absence of incidents."
```

That language actually sounds **more credible**.

---

## 17. And here's what I think DarkOps' identity becomes

Not:

> **"Another cybersecurity platform."**

More like:

> **DarkOps is the security operations layer for applications.**

The application says:

```text
"Here is the security state
 I'm authorizing you to see."
```

DarkOps says:

```text
"I'll continuously understand it."
```

Something changes:

```text
Event
 ↓
Analysis
 ↓
Context
 ↓
Alert
 ↓
Incident
 ↓
Response
 ↓
Audit
```

And the business gets:

```text
Less manual security work
+
Better visibility
+
Faster investigation
+
Structured response
+
Historical evidence
+
Controlled application access
```

That's the product.

And **that** is what we should now use to judge every future feature.

If a proposed feature doesn't strengthen that core, we ask:

> **"Why the hell are we building this?"**

That question will save us a *lot* more time than trying to finish 26 resources just because they're already sitting in `vault/resources`.

One more thing: the product comparison above is a **category/positioning comparison, not a claim that DarkOps is currently equivalent to those mature platforms**. Microsoft, Wazuh, Splunk, Snyk, Palo Alto and Wiz already have extensive production capabilities; DarkOps is defining a narrower application-centric product boundary. Their current product descriptions support the distinctions above.

This is the kind of foundation I'd lock **before touching the remaining resources**.
