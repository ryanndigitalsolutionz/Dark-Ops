import { HeroSection } from "@/components/blocks/hero-section"

function HeroSectionDemo() {
  return (
    <HeroSection
      title="DarkOps Security Platform"
      subtitle={{
        regular: "Security for the systems ",
        gradient: "you entrust.",
      }}
      description="Monitor security activity, investigate incidents, and maintain visibility across the applications and systems connected to DarkOps."
      loginHref="/login"
      signupHref="/signup"
      gridOptions={{
        angle: 65,
        opacity: 0.35,
        cellSize: 50,
        lightLineColor: "#8A8580",
        darkLineColor: "#8A8580",
      }}
    />
  )
}

export { HeroSectionDemo }
