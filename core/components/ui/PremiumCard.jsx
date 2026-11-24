
export default function PremiumCard({
  children,
  className = "",
  contentClassName = "",
  gradient,
  padding = "md",
  radius = "xl",
}) {
  const paddings = {
    none: "p-0",
    sm: "p-3",
    md: "p-5",
    lg: "p-7",
  };

  const radiuses = {
    lg: "rounded-lg",
    xl: "rounded-xl",
    "2xl": "rounded-2xl",
  };

  const borderGradient =
    gradient ||
    "linear-gradient(135deg, var(--color-agency-orange), #dc2626 50%, #713f32)";

  return (
    <div
      className={`relative ${radiuses[radius] || radiuses.xl} p-px ${className}`}
      style={{ background: borderGradient }}
    >
      <div
        className={`h-full w-full bg-[var(--color-agency-card)] ${
          radiuses[radius] || radiuses.xl
        } ${paddings[padding] || paddings.md} ${contentClassName}`}
      >
        {children}
      </div>
    </div>
  );
}
