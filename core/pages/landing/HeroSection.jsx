import * as React from "react"
import { Link } from "react-router"
import { cn } from "@/lib/utils"
import { FiChevronRight } from "react-icons/fi";
import DashboardPreview from "../center/homepage/DashboardPreview";

const RetroGrid = ({
  angle = 65,
  cellSize = 60,
  opacity = 0.35,
  lightLineColor = "#8A8580",
  darkLineColor = "#8A8580",
}) => {
  const gridStyles = {
    "--grid-angle": `${angle}deg`,
    "--cell-size": `${cellSize}px`,
    "--opacity": opacity,
    "--light-line": lightLineColor,
    "--dark-line": darkLineColor,
  }

  return (
    <div
      className={cn(
        "pointer-events-none absolute size-full overflow-hidden [perspective:200px]",
        "opacity-[var(--opacity)]",
      )}
      style={gridStyles}
    >
      <div className="absolute inset-0 [transform:rotateX(var(--grid-angle))]">
        <div
          className="
            animate-grid
            [background-image:linear-gradient(to_right,var(--light-line)_1px,transparent_0),linear-gradient(to_bottom,var(--light-line)_1px,transparent_0)]
            [background-repeat:repeat]
            [background-size:var(--cell-size)_var(--cell-size)]
            [height:300vh]
            [inset:0%_0px]
            [margin-left:-200%]
            [transform-origin:100%_0_0]
            [width:600vw]
            dark:[background-image:linear-gradient(to_right,var(--dark-line)_1px,transparent_0),linear-gradient(to_bottom,var(--dark-line)_1px,transparent_0)]
          "
        />
      </div>

      <div className="absolute inset-0 bg-gradient-to-t from-white via-white/80 to-transparent to-90% dark:from-[#1A1A1A] dark:via-[#1A1A1A]/80" />
    </div>
  )
}

const HeroSection = React.forwardRef(
  (
    {
      className,
      title = "DarkOps Security Platform",
      subtitle = {
        regular: "Security for the systems ",
        gradient: "you entrust.",
      },
      description = (
        "Monitor security activity, investigate incidents, "
        + "and maintain visibility across the applications and systems connected to DarkOps."
      ),
      loginHref = "/login",
      signupHref = "/signup",
      bottomImage,
      gridOptions,
      ...props
    },
    ref,
  ) => {
    return (
      <div
        className={cn(
          "relative min-h-screen overflow-hidden bg-white text-[#1A1A1A] dark:bg-[#1A1A1A] dark:text-white",
          className,
        )}
        ref={ref}
        {...props}
      >
        {/* Subtle top atmosphere */}
        <div
          className="
            absolute top-0 z-0 h-screen w-screen
            bg-[#C65A24]/5
            [background:radial-gradient(ellipse_25%_75%_at_50%_-20%,rgba(198,90,36,0.14),rgba(255,255,255,0))]
            dark:bg-[#C65A24]/5
            dark:[background:radial-gradient(ellipse_25%_75%_at_50%_-20%,rgba(198,90,36,0.18),rgba(26,26,26,0))]
          "
        />

        <section className="relative z-[1] mx-auto max-w-full">
          <RetroGrid {...gridOptions} />

          <div className="relative z-10 mx-auto max-w-screen-xl px-4 py-28 md:px-8">
            <div className="mx-auto max-w-4xl space-y-6 text-center">

              {/* Small identity badge */}
              <div
                className="
                  group mx-auto flex w-fit items-center gap-2
                  rounded-3xl
                  border border-[#1A1A1A]/10
                  bg-gradient-to-tr from-[#8A8580]/10 via-[#C65A24]/10 to-transparent
                  px-5 py-2
                  text-sm text-[#8A8580]
                  dark:border-white/10
                  dark:from-[#8A8580]/5
                  dark:via-[#C65A24]/10
                  dark:text-[#B6B1AC]
                "
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                <span>DarkOps</span>

                <FiChevronRight
                  className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1"
                />
              </div>

              {/* Main heading */}
              <h1
                className="
                  mx-auto
                  max-w-4xl
                  text-5xl
                  tracking-tight
                  text-[#1A1A1A]
                  dark:text-white
                  md:text-7xl
                "
                style={{ fontFamily: "Foldit, sans-serif" }}
              >
                {subtitle.regular}

                <span
                  className="
                    bg-gradient-to-r
                    from-[#C65A24]
                    via-[#D6783C]
                    to-[#8A8580]
                    bg-clip-text
                    text-transparent
                  "
                >
                  {subtitle.gradient}
                </span>
              </h1>

              {/* Description */}
              <p
                className="
                  mx-auto
                  max-w-2xl
                  text-base
                  leading-7
                  text-[#8A8580]
                  dark:text-[#B6B1AC]
                  md:text-lg
                "
                style={{ fontFamily: "Inter, sans-serif" }}
              >
                {description}
              </p>

              {/* Authentication actions */}
              <div
                className="flex items-center justify-center gap-3 pt-3"
                style={{ fontFamily: "Inter, sans-serif" }}
              >

                {/* Log In */}
                <Link
                  to={loginHref}
                  className="
                    group
                    inline-flex
                    items-center
                    justify-center
                    rounded-full
                    border
                    border-[#8A8580]/30
                    bg-white/70
                    px-7
                    py-3.5
                    text-sm
                    font-medium
                    text-[#1A1A1A]
                    shadow-sm
                    backdrop-blur-xl
                    transition-all
                    duration-300
                    hover:-translate-y-0.5
                    hover:border-[#C65A24]/50
                    hover:bg-[#C65A24]/5
                    dark:border-[#8A8580]/30
                    dark:bg-[#1A1A1A]/70
                    dark:text-white
                    dark:hover:bg-[#C65A24]/10
                  "
                >
                  Log In
                </Link>

                {/* Sign Up */}
                <span className="relative inline-block overflow-hidden rounded-full p-[1.5px]">
                  <span
                    className="
                      absolute
                      inset-[-1000%]
                      animate-[spin_2s_linear_infinite]
                      bg-[conic-gradient(from_90deg_at_50%_50%,#8A8580_0%,#C65A24_50%,#8A8580_100%)]
                    "
                  />

                  <Link
                    to={signupHref}
                    className="
                      relative
                      inline-flex
                      items-center
                      justify-center
                      rounded-full
                      bg-[#1A1A1A]
                      px-7
                      py-3.5
                      text-sm
                      font-medium
                      text-white
                      transition-all
                      duration-300
                      hover:bg-[#C65A24]
                      dark:bg-white
                      dark:text-[#1A1A1A]
                      dark:hover:bg-[#C65A24]
                      dark:hover:text-white
                    "
                  >
                    Sign Up
                  </Link>
                </span>
              </div>

              <div className="relative z-10 mx-2 mt-28 md:mx-6">
  <DashboardPreview />
</div>
            </div>
          </div>
        </section>
      </div>
    )
  },
)

HeroSection.displayName = "HeroSection"

export default HeroSection;
