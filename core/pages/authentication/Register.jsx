import { useMemo, useState } from "react";
import {
  FiCalendar,
  FiCheck,
  FiChevronDown,
  FiEye,
  FiEyeOff,
} from "react-icons/fi";

const COUNTRIES = [
  { name: "Kenya", flag: "🇰🇪", code: "+254" },
  { name: "United States", flag: "🇺🇸", code: "+1" },
  { name: "United Kingdom", flag: "🇬🇧", code: "+44" },
  { name: "South Africa", flag: "🇿🇦", code: "+27" },
  { name: "Nigeria", flag: "🇳🇬", code: "+234" },
  { name: "Ghana", flag: "🇬🇭", code: "+233" },
  { name: "Tanzania", flag: "🇹🇿", code: "+255" },
  { name: "Uganda", flag: "🇺🇬", code: "+256" },
  { name: "Rwanda", flag: "🇷🇼", code: "+250" },
  { name: "Canada", flag: "🇨🇦", code: "+1" },
  { name: "Germany", flag: "🇩🇪", code: "+49" },
  { name: "France", flag: "🇫🇷", code: "+33" },
  { name: "India", flag: "🇮🇳", code: "+91" },
  { name: "United Arab Emirates", flag: "🇦🇪", code: "+971" },
];

const PRONOUNS = ["He/him", "She/her", "Rather not say"];

function PasswordRequirement({ met, children }) {
  return (
    <div className={`password-rule ${met ? "met" : ""}`}>
      <span className="password-rule-icon">
        {met && <FiCheck size={12} />}
      </span>
      <span>{children}</span>
    </div>
  );
}

export default function Register() {
  const [country, setCountry] = useState(COUNTRIES[0]);
  const [pronouns, setPronouns] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    dateOfBirth: "",
    email: "",
    phone: "",
    username: "",
    password: "",
    agreement: false,
  });

  const username = form.username.trim();

  const passwordRules = useMemo(
    () => ({
      length: form.password.length >= 6,
      uppercase: /[A-Z]/.test(form.password),
      lowercase: /[a-z]/.test(form.password),
      number: /\d/.test(form.password),
    }),
    [form.password]
  );

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    setForm((current) => ({
      ...current,
      [name]:
        type === "checkbox"
          ? checked
          : name === "username"
            ? value.toLowerCase().replace(/\s/g, "")
            : value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (username.length < 2 || !passwordRules.length || !form.agreement) {
      return;
    }

    // Registration API integration will go here.
  };

  return (
    <div className="register-page">
      <div className="register-overlay" />

      <main className="register-shell">
        <section className="register-card">
          <header className="register-header">
            <h1 className="register-welcome">
              Welcome{username ? ` ${username}` : ""}
            </h1>
            <p className="register-subtitle">
              Let's get your DarkOps account ready.
            </p>
          </header>

          <form onSubmit={handleSubmit} className="register-form">
            <div className="field-group full">
              <label htmlFor="country">Country / Region</label>

              <div className="select-wrapper country-select">
                <span className="select-leading">{country.flag}</span>

                <select
                  id="country"
                  value={country.name}
                  onChange={(event) => {
                    const selected = COUNTRIES.find(
                      (item) => item.name === event.target.value
                    );

                    if (selected) setCountry(selected);
                  }}
                >
                  {COUNTRIES.map((item) => (
                    <option key={item.name} value={item.name}>
                      {item.name}
                    </option>
                  ))}
                </select>

                <FiChevronDown className="select-chevron" />
              </div>
            </div>

            <div className="form-grid">
              <div className="field-group">
                <label htmlFor="pronouns">Pronouns</label>

                <div className="select-wrapper">
                  <select
                    id="pronouns"
                    value={pronouns}
                    onChange={(event) => setPronouns(event.target.value)}
                  >
                    <option value="">Select</option>
                    {PRONOUNS.map((item) => (
                      <option key={item} value={item}>
                        {item}
                      </option>
                    ))}
                  </select>

                  <FiChevronDown className="select-chevron" />
                </div>
              </div>

              <div className="field-group">
                <label htmlFor="firstName">First Name</label>

                <input
                  id="firstName"
                  name="firstName"
                  value={form.firstName}
                  onChange={handleChange}
                  autoComplete="given-name"
                  required
                />

                <span className="field-note">
                  As per your Passport / Government ID
                </span>
              </div>
            </div>

            <div className="form-grid">
              <div className="field-group">
                <label htmlFor="lastName">Last Name</label>

                <input
                  id="lastName"
                  name="lastName"
                  value={form.lastName}
                  onChange={handleChange}
                  autoComplete="family-name"
                  required
                />
              </div>

              <div className="field-group">
                <label htmlFor="dateOfBirth">Date of Birth</label>

                <div className="date-wrapper">
                  <FiCalendar className="date-icon" />

                  <input
                    id="dateOfBirth"
                    name="dateOfBirth"
                    type="date"
                    value={form.dateOfBirth}
                    onChange={handleChange}
                    autoComplete="bday"
                    required
                  />
                </div>
              </div>
            </div>

            <div className="form-grid">
              <div className="field-group">
                <label htmlFor="email">Email address</label>

                <input
                  id="email"
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={handleChange}
                  autoComplete="email"
                  required
                />
              </div>

              <div className="field-group">
                <label htmlFor="phone">Phone number</label>

                <div className="phone-wrapper">
                  <div className="phone-country">
                    <span>{country.flag}</span>
                    <span>{country.code}</span>
                    <FiChevronDown />
                  </div>

                  <input
                    id="phone"
                    name="phone"
                    type="tel"
                    value={form.phone}
                    onChange={handleChange}
                    autoComplete="tel"
                    required
                  />
                </div>
              </div>
            </div>

            <div className="field-group full">
              <label htmlFor="username">Unique Username</label>

              <input
                id="username"
                name="username"
                type="text"
                minLength={2}
                maxLength={30}
                pattern="[a-z0-9._-]+"
                title="Use lowercase letters, numbers, periods, underscores, or hyphens."
                value={form.username}
                onChange={handleChange}
                autoComplete="username"
                placeholder="Choose your permanent username"
                required
              />

              <span className="field-note">
                Minimum 2 characters. Choose carefully: your username cannot
                be changed after registration.
              </span>
            </div>

            <div className="field-group full">
              <label htmlFor="password">Create your account password</label>

              <div className="password-wrapper">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={handleChange}
                  autoComplete="new-password"
                  minLength={6}
                  required
                />

                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((current) => !current)}
                  aria-label={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? <FiEyeOff /> : <FiEye />}
                </button>
              </div>

              <div className="password-rules">
                <PasswordRequirement met={passwordRules.length}>
                  At least 6 characters
                </PasswordRequirement>

                <PasswordRequirement met={passwordRules.uppercase}>
                  One uppercase letter
                </PasswordRequirement>

                <PasswordRequirement met={passwordRules.lowercase}>
                  One lowercase letter
                </PasswordRequirement>

                <PasswordRequirement met={passwordRules.number}>
                  One number
                </PasswordRequirement>
              </div>

              <p className="password-help">
                Only the 6-character minimum is required — the rest make your
                password stronger.
              </p>
            </div>

            <label className="agreement-row">
              <input
                type="checkbox"
                name="agreement"
                checked={form.agreement}
                onChange={handleChange}
                required
              />

              <span className="agreement-box" />

              <span className="agreement-text">
                I confirm I've read and agree with the{" "}
                <a href="/policies/withdrawal-refund">
                  Withdrawal &amp; Refund Policy
                </a>
                , <a href="/policies/terms">Terms &amp; Conditions</a>,{" "}
                <a href="/policies/complaint-handling">
                  Complaint Handling Procedure
                </a>
                ,{" "}
                <a href="/policies/conflicts-of-interest">
                  Conflicts of Interest Policy
                </a>
                , <a href="/policies/cookies">Cookies Policy</a>,{" "}
                <a href="/policies/market-abuse">Market Abuse Policy</a> and
                Acknowledgment, Overnight Charges Policy and all applicable
                DarkOps policies.
              </span>
            </label>

            <button
              type="submit"
              className="register-submit"
              disabled={!form.agreement}
            >
              Create Account
            </button>
          </form>
        </section>
      </main>

      <style>{`
        .register-page {
          position: relative;
          min-height: 100vh;
          padding: 0 24px 48px;
          overflow-x: hidden;
          background: url("/assets/decoration/milad-fakurian-VbC-EiOTDqA-unsplash.jpg") center / cover fixed no-repeat;
          color: #E8E5E2;
          font-family: "Montserrat Alternates", sans-serif;
        }

        .register-overlay {
          position: fixed;
          inset: 0;
          pointer-events: none;
          background: rgba(8, 8, 8, 0.72);
        }

        .register-shell {
          position: relative;
          z-index: 1;
          width: min(100%, 862px);
          margin: 0 auto;
        }

        .register-card {
          padding: 30px 40px 42px;
          border: 1px solid #41413E;
          border-top: 0;
          border-radius: 0 0 22px 22px;
          background: rgba(29, 29, 28, 0.97);
          box-shadow: 0 26px 80px rgba(0, 0, 0, 0.4);
          backdrop-filter: blur(18px);
        }

        .register-header {
          margin-bottom: 26px;
        }

        .register-welcome {
          margin: 0;
          color: #F3F1EF;
          overflow-wrap: anywhere;
          font-family: "Montserrat Alternates", sans-serif;
          font-size: clamp(1.45rem, 2.5vw, 1.85rem);
          font-weight: 700;
          line-height: 1.3;
          letter-spacing: -0.035em;
        }

        .register-subtitle {
          margin: 7px 0 0;
          color: #AAA49D;
          font-size: 0.82rem;
          line-height: 1.5;
        }

        .register-form {
          display: flex;
          flex-direction: column;
          gap: 18px;
        }

        .form-grid {
          display: grid;
          grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
          gap: 22px;
        }

        .field-group {
          min-width: 0;
        }

        .field-group.full {
          width: 100%;
        }

        .field-group > label {
          display: block;
          margin-bottom: 7px;
          color: #C4C0BB;
          font-size: 0.84rem;
          font-weight: 600;
        }

        .field-group > input,
        .field-group select {
          width: 100%;
          height: 62px;
          box-sizing: border-box;
          border: 1px solid #4A4945;
          border-radius: 15px;
          outline: none;
          background: #222220;
          color: #F3F1EF;
          font-family: "Montserrat Alternates", sans-serif;
          font-size: 0.96rem;
          transition: border-color 160ms ease, box-shadow 160ms ease;
        }

        .field-group > input {
          padding: 0 19px;
        }

        .field-group input::placeholder {
          color: #96908A;
        }

        .field-group input:focus,
        .field-group select:focus {
          border-color: #C65A24;
          box-shadow: 0 0 0 3px rgba(198, 90, 36, 0.13);
        }

        .select-wrapper,
        .date-wrapper,
        .password-wrapper {
          position: relative;
        }

        .select-wrapper select {
          appearance: none;
          padding: 0 48px 0 19px;
          cursor: pointer;
        }

        .country-select select {
          padding-left: 55px;
        }

        .select-leading {
          position: absolute;
          top: 50%;
          left: 20px;
          z-index: 1;
          transform: translateY(-50%);
          font-size: 1.15rem;
          pointer-events: none;
        }

        .select-chevron {
          position: absolute;
          top: 50%;
          right: 18px;
          z-index: 1;
          transform: translateY(-50%);
          color: #B6B1AC;
          pointer-events: none;
        }

        .field-note {
          display: block;
          margin-top: 6px;
          color: #AAA49D;
          font-size: 0.74rem;
          line-height: 1.55;
        }

        .date-wrapper input {
          width: 100%;
          height: 62px;
          padding: 0 14px 0 55px;
          box-sizing: border-box;
          border: 1px solid #4A4945;
          border-radius: 15px;
          outline: none;
          background: #222220;
          color: #F3F1EF;
          font-family: inherit;
          font-size: 0.96rem;
          color-scheme: dark;
        }

        .date-wrapper input:focus {
          border-color: #C65A24;
          box-shadow: 0 0 0 3px rgba(198, 90, 36, 0.13);
        }

        .date-icon {
          position: absolute;
          top: 50%;
          left: 21px;
          z-index: 1;
          transform: translateY(-50%);
          color: #D6783C;
          pointer-events: none;
        }

        .phone-wrapper {
          display: flex;
          height: 62px;
          overflow: hidden;
          border: 1px solid #4A4945;
          border-radius: 15px;
          background: #222220;
        }

        .phone-wrapper:focus-within {
          border-color: #C65A24;
          box-shadow: 0 0 0 3px rgba(198, 90, 36, 0.13);
        }

        .phone-country {
          display: flex;
          align-items: center;
          gap: 8px;
          flex: 0 0 auto;
          padding: 0 12px;
          border-right: 1px solid #4A4945;
          color: #E8E5E2;
          font-size: 0.83rem;
          white-space: nowrap;
        }

        .phone-country > span:first-child {
          font-size: 1rem;
        }

        .phone-country svg {
          color: #B6B1AC;
        }

        .phone-wrapper input {
          min-width: 0;
          width: 100%;
          height: 100%;
          padding: 0 14px;
          border: 0;
          outline: none;
          background: transparent;
          color: #F3F1EF;
          font: inherit;
        }

        .phone-wrapper input:focus {
          box-shadow: none;
        }

        .password-wrapper input {
          padding-right: 58px;
        }

        .password-toggle {
          position: absolute;
          top: 50%;
          right: 18px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          padding: 0;
          border: 0;
          background: transparent;
          color: #B6B1AC;
          font-size: 21px;
          transform: translateY(-50%);
          cursor: pointer;
        }

        .password-toggle:hover {
          color: #D6783C;
        }

        .password-rules {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 8px 25px;
          margin-top: 12px;
        }

        .password-rule {
          display: flex;
          align-items: center;
          gap: 10px;
          color: #B6B1AC;
          font-size: 0.8rem;
        }

        .password-rule.met {
          color: #D6783C;
        }

        .password-rule-icon {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 21px;
          height: 21px;
          flex: 0 0 21px;
          border: 1px solid #77716B;
          border-radius: 50%;
          box-sizing: border-box;
        }

        .password-rule.met .password-rule-icon {
          border-color: #D6783C;
          background: rgba(198, 90, 36, 0.12);
        }

        .password-help {
          margin: 7px 0 0;
          color: #AAA49D;
          font-size: 0.75rem;
          line-height: 1.5;
        }

        .agreement-row {
          position: relative;
          display: grid;
          grid-template-columns: 32px minmax(0, 1fr);
          gap: 14px;
          align-items: start;
          cursor: pointer;
        }

        .agreement-row input {
          position: absolute;
          width: 1px;
          height: 1px;
          opacity: 0;
        }

        .agreement-box {
          position: relative;
          width: 28px;
          height: 28px;
          margin-top: 2px;
          border: 1px solid #8A8580;
          border-radius: 4px;
          background: #E8E5E2;
          box-sizing: border-box;
        }

        .agreement-row input:checked + .agreement-box {
          border-color: #C65A24;
          background: #C65A24;
        }

        .agreement-row input:checked + .agreement-box::after {
          content: "";
          position: absolute;
          top: 4px;
          left: 9px;
          width: 7px;
          height: 13px;
          border: solid #FFFFFF;
          border-width: 0 2px 2px 0;
          transform: rotate(45deg);
        }

        .agreement-row input:focus-visible + .agreement-box {
          outline: 2px solid #D6783C;
          outline-offset: 3px;
        }

        .agreement-text {
          color: #D6D2CE;
          font-size: 0.77rem;
          line-height: 1.75;
        }

        .agreement-text a {
          color: #D6783C;
          font-weight: 600;
          text-decoration: none;
        }

        .agreement-text a:hover {
          color: #E79563;
          text-decoration: underline;
        }

        .register-submit {
          width: 100%;
          min-height: 58px;
          margin-top: 2px;
          border: 1px solid #C65A24;
          border-radius: 14px;
          background: #C65A24;
          color: #FFFFFF;
          font-family: "Montserrat Alternates", sans-serif;
          font-size: 0.92rem;
          font-weight: 700;
          cursor: pointer;
          transition: background 160ms ease, transform 160ms ease;
        }

        .register-submit:hover:not(:disabled) {
          background: #D6783C;
          transform: translateY(-1px);
        }

        .register-submit:disabled {
          border-color: #5A514B;
          background: #49423D;
          color: #C0B8B1;
          cursor: not-allowed;
        }

        @media (max-width: 700px) {
          .register-page {
            padding: 0 12px 28px;
            background-attachment: scroll;
          }

          .register-card {
            padding: 25px 20px 30px;
          }

          .form-grid {
            grid-template-columns: minmax(0, 1fr);
            gap: 18px;
          }

          .password-rules {
            grid-template-columns: 1fr;
          }

          .agreement-row {
            grid-template-columns: 28px minmax(0, 1fr);
            gap: 11px;
          }

          .agreement-text {
            font-size: 0.73rem;
          }
        }
      `}</style>
    </div>
  );
}
