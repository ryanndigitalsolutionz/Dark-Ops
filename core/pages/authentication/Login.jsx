// Login.jsx
import { useEffect, useState } from "react";
import { FiEye, FiEyeOff, FiKey, FiLock } from "react-icons/fi";

const BACKGROUND_IMAGE =
  "/assets/decoration/milad-fakurian-VbC-EiOTDqA-unsplash.jpg";

const U1_BADGE = "/assets/decoration/U1_ID.svg";

function GoogleMark() {
  return (
    <span
      className="text-lg font-bold"
      style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
      aria-hidden="true"
    >
      G
    </span>
  );
}

function MicrosoftMark() {
  return (
    <span
      className="grid grid-cols-2 gap-[2px]"
      aria-hidden="true"
    >
      <span className="h-[7px] w-[7px] bg-[#F35325]" />
      <span className="h-[7px] w-[7px] bg-[#81BC06]" />
      <span className="h-[7px] w-[7px] bg-[#05A6F0]" />
      <span className="h-[7px] w-[7px] bg-[#FFBA08]" />
    </span>
  );
}

export default function Login() {
  const [u1Id, setU1Id] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [agreed, setAgreed] = useState(false);

  useEffect(() => {
    document.title = "Sign In · DarkOps";
  }, []);

  return (
    <main
      className="
        relative flex min-h-screen items-center justify-center
        overflow-hidden
        bg-[#0B0C0E]
        px-4 py-8
        text-white
      "
      style={{
        backgroundImage: `url("${BACKGROUND_IMAGE}")`,
        backgroundPosition: "center",
        backgroundSize: "cover",
      }}
    >
      {/* Background overlay */}
      <div
        className="
          absolute inset-0
          bg-[#0B0C0E]/82
          backdrop-blur-[3px]
        "
      />

      <div
        className="
          absolute inset-0
          bg-[radial-gradient(circle_at_top,rgba(198,90,36,0.18),transparent_48%)]
        "
      />

      {/* Login card */}
      <section
        className="
          relative z-10
          w-full max-w-md
          overflow-hidden
          rounded-3xl
          border border-white/10
          bg-[#111416]/92
          shadow-2xl shadow-black/50
          backdrop-blur-2xl
        "
      >
        <div className="px-6 pb-7 pt-8 sm:px-8">

        {/* DarkOps Wordmark */}
        <div
        className="
            mx-auto
            flex
            h-24
            w-3/4
            items-center
            justify-center
            overflow-hidden
        "
        >
        <img
            src="/logo/woodmark/brand-name.svg"
            alt="DarkOps"
            className="
            h-[300%]
            w-[300%]
            max-w-none
            shrink-0
            object-contain
            "
        />
        </div>

          {/* Heading */}
          <div className="mt-4 text-center">
            <h1
              className="text-4xl tracking-tight text-white"
              style={{ fontFamily: "Foldit, sans-serif" }}
            >
              Welcome back.
            </h1>

            <p
              className="mt-2 text-sm leading-6 text-white/55"
              style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
            >
              Sign in to continue to DarkOps.
            </p>
          </div>

          {/* OAuth */}
          <div
            className="mt-7 grid gap-3"
            style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
          >
            <button
              type="button"
              disabled
              className="
                flex min-h-12 items-center justify-center gap-3
                rounded-xl
                border border-white/10
                bg-white/[0.035]
                px-4
                text-sm font-semibold text-white/40
                cursor-not-allowed
              "
            >
              <GoogleMark />
              Continue with Google
            </button>

            <button
              type="button"
              disabled
              className="
                flex min-h-12 items-center justify-center gap-3
                rounded-xl
                border border-white/10
                bg-white/[0.035]
                px-4
                text-sm font-semibold text-white/40
                cursor-not-allowed
              "
            >
              <MicrosoftMark />
              Continue with Microsoft
            </button>
          </div>

          {/* Divider */}
          <div
            className="
              my-6 flex items-center gap-3
              text-[10px] uppercase tracking-[0.18em]
              text-white/25
            "
            style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
          >
            <span className="h-px flex-1 bg-white/10" />
            <span>or use your credentials</span>
            <span className="h-px flex-1 bg-white/10" />
          </div>

          <form
            onSubmit={(event) => event.preventDefault()}
            className="space-y-4"
            style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
          >
            {/* U1 ID */}
            <div>
              <label
                htmlFor="login-u1-id"
                className="mb-2 block text-xs font-semibold text-white/70"
              >
                U1 ID
              </label>

              <div
                className="
                  flex min-h-14 items-center
                  rounded-xl
                  border border-white/10
                  bg-white/[0.035]
                  transition-colors
                  focus-within:border-[#C65A24]/70
                  focus-within:ring-2
                  focus-within:ring-[#C65A24]/10
                "
              >
                <div className="flex w-14 shrink-0 items-center justify-center border-r border-white/10">
                  <img
                    src={U1_BADGE}
                    alt=""
                    className="h-7 w-7 object-contain"
                  />
                </div>

                <input
                  id="login-u1-id"
                  name="u1Id"
                  type="text"
                  value={u1Id}
                  onChange={(event) => setU1Id(event.target.value)}
                  autoComplete="username"
                  placeholder="Enter your U1 ID"
                  className="
                    min-w-0 flex-1
                    bg-transparent
                    px-4
                    text-sm text-white
                    outline-none
                    placeholder:text-white/25
                  "
                />
              </div>
            </div>

            {/* Credential divider */}
            <div className="flex items-center gap-3 py-1">
              <span className="h-px flex-1 bg-white/10" />

              <span
                className="
                  text-[10px]
                  uppercase
                  tracking-[0.16em]
                  text-white/25
                "
                style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
              >
                Email & Password
              </span>

              <span className="h-px flex-1 bg-white/10" />
            </div>

            {/* Email */}
            <div>
              <label
                htmlFor="login-email"
                className="mb-2 block text-xs font-semibold text-white/70"
              >
                Email
              </label>

              <div
                className="
                  flex min-h-14 items-center
                  rounded-xl
                  border border-white/10
                  bg-white/[0.035]
                  transition-colors
                  focus-within:border-[#C65A24]/70
                  focus-within:ring-2
                  focus-within:ring-[#C65A24]/10
                "
              >
                <FiKey className="ml-4 h-4 w-4 shrink-0 text-white/35" />

                <input
                  id="login-email"
                  name="email"
                  type="email"
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  autoComplete="email"
                  placeholder="you@example.com"
                  className="
                    min-w-0 flex-1
                    bg-transparent
                    px-3 pr-4
                    text-sm text-white
                    outline-none
                    placeholder:text-white/25
                  "
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label
                htmlFor="login-password"
                className="mb-2 block text-xs font-semibold text-white/70"
              >
                Password
              </label>

              <div
                className="
                  relative
                  flex min-h-14 items-center
                  rounded-xl
                  border border-white/10
                  bg-white/[0.035]
                  transition-colors
                  focus-within:border-[#C65A24]/70
                  focus-within:ring-2
                  focus-within:ring-[#C65A24]/10
                "
              >
                <FiLock className="ml-4 h-4 w-4 shrink-0 text-white/35" />

                <input
                  id="login-password"
                  name="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  autoComplete="current-password"
                  placeholder="Enter your password"
                  className="
                    min-w-0 flex-1
                    bg-transparent
                    px-3 pr-12
                    text-sm text-white
                    outline-none
                    placeholder:text-white/25
                  "
                />

                <button
                  type="button"
                  onClick={() => setShowPassword((current) => !current)}
                  className="
                    absolute right-2
                    grid h-10 w-10 place-items-center
                    rounded-lg
                    text-white/45
                    transition-colors
                    hover:bg-white/5
                    hover:text-white
                  "
                  aria-label={showPassword ? "Hide password" : "Show password"}
                  title={showPassword ? "Hide password" : "Show password"}
                >
                  {showPassword ? (
                    <FiEyeOff className="h-4 w-4" />
                  ) : (
                    <FiEye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Remember + Forgot */}
            <div className="flex items-center justify-between gap-4 pt-1">
              <label className="flex items-center gap-2 text-xs text-white/50">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(event) => setRememberMe(event.target.checked)}
                  className="h-4 w-4 accent-[#C65A24]"
                />
                Remember me
              </label>

              <button
                type="button"
                disabled
                className="
                  text-xs font-semibold
                  text-[#D6783C]/45
                  cursor-not-allowed
                "
              >
                Forgot Password?
              </button>
            </div>

            {/* Sign In */}
            <button
              type="submit"
              disabled
              className="
                mt-2 flex min-h-14 w-full items-center justify-center
                rounded-xl
                bg-[#C65A24]/35
                px-5
                text-sm font-bold
                text-white/45
                cursor-not-allowed
              "
            >
              Sign In
            </button>
          </form>

          {/* Register */}
          <div
            className="
              mt-6 text-center
              text-sm text-white/45
            "
            style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
          >
            Haven't registered yet?{" "}
            <button
              type="button"
              disabled
              className="
                font-semibold
                text-[#D6783C]/45
                cursor-not-allowed
              "
            >
              Sign up!
            </button>
          </div>

          {/* Agreement */}
          <label
            className="
              mt-6 flex items-start gap-3
              border-t border-white/10
              pt-5
              text-[11px] leading-5
              text-white/40
            "
            style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
          >
            <input
              type="checkbox"
              checked={agreed}
              onChange={(event) => setAgreed(event.target.checked)}
              className="mt-0.5 h-4 w-4 shrink-0 accent-[#C65A24]"
            />

            <span>
              I have agreed to the{" "}
              <span className="text-white/60 underline underline-offset-2">
                Terms of Service
              </span>{" "}
              and{" "}
              <span className="text-white/60 underline underline-offset-2">
                Privacy Policy
              </span>
              .
            </span>
          </label>
        </div>

        {/* Footer */}
        <div
          className="
            border-t border-white/10
            px-6 py-4
            text-center
            text-[10px]
            uppercase
            tracking-[0.16em]
            text-white/20
          "
          style={{ fontFamily: "Montserrat Alternates, sans-serif" }}
        >
          DarkOps · Security for the systems you entrust.
        </div>
      </section>
    </main>
  );
}
