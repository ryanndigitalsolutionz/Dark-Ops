import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const securityActivity = [
  { time: "00:00", events: 18 },
  { time: "04:00", events: 25 },
  { time: "08:00", events: 41 },
  { time: "12:00", events: 34 },
  { time: "16:00", events: 58 },
  { time: "20:00", events: 46 },
  { time: "24:00", events: 67 },
];

const montserrat = {
  fontFamily: "Montserrat Alternates, sans-serif",
};

const foldit = {
  fontFamily: "Foldit, sans-serif",
};

function StatCard({ label, value, detail }) {
  return (
    <div className="rounded-xl border border-[#8A8580]/20 bg-white/70 p-5 backdrop-blur-xl dark:bg-[#151515]/80">
      <p
        className="text-xs font-medium uppercase tracking-wider text-[#8A8580]"
        style={montserrat}
      >
        {label}
      </p>

      <p
        className="mt-2 text-2xl font-semibold text-[#1A1A1A] dark:text-white"
        style={montserrat}
      >
        {value}
      </p>

      {detail && (
        <p
          className="mt-1 text-xs text-[#8A8580]"
          style={montserrat}
        >
          {detail}
        </p>
      )}
    </div>
  );
}

function DashboardPreview() {
  return (
    <div className="overflow-hidden rounded-2xl border border-[#8A8580]/25 bg-white/80 shadow-2xl backdrop-blur-2xl dark:bg-[#111111]/90">

      {/* Header */}
      <div className="flex items-center justify-between border-b border-[#8A8580]/20 px-6 py-4">
        <div>
          <p
            className="text-xs uppercase tracking-[0.2em] text-[#8A8580]"
            style={montserrat}
          >
            DarkOps
          </p>

          <h3
            className="mt-1 text-lg text-[#1A1A1A] dark:text-white"
            style={foldit}
          >
            Security Command Center
          </h3>
        </div>

        <div
          className="flex items-center gap-2 text-xs text-[#8A8580]"
          style={montserrat}
        >
          <span className="h-2 w-2 rounded-full bg-green-500" />
          Systems Operational
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-2 gap-3 p-5 md:grid-cols-4">
        <StatCard
          label="Security Posture"
          value="92%"
          detail="Overall state"
        />

        <StatCard
          label="Incidents"
          value="3"
          detail="1 requires action"
        />

        <StatCard
          label="Open Alerts"
          value="12"
          detail="Across 8 assets"
        />

        <StatCard
          label="Applications"
          value="18"
          detail="17 protected"
        />
      </div>

      {/* Security Activity */}
      <div className="mx-5 mb-5 rounded-xl border border-[#8A8580]/20 bg-black/[0.02] p-5 dark:bg-white/[0.02]">
        <div className="mb-5">
          <p
            className="text-xs uppercase tracking-[0.15em] text-[#8A8580]"
            style={montserrat}
          >
            Security Activity
          </p>

          <div className="mt-1 flex items-end justify-between">
            <h4
              className="text-xl text-[#1A1A1A] dark:text-white"
              style={foldit}
            >
              Events detected
            </h4>

            <span
              className="text-xs text-[#8A8580]"
              style={montserrat}
            >
              Last 24 hours
            </span>
          </div>
        </div>

        <div className="h-[240px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={securityActivity}>
              <defs>
                <linearGradient
                  id="darkOpsActivity"
                  x1="0"
                  y1="0"
                  x2="0"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopColor="#C65A24"
                    stopOpacity={0.35}
                  />

                  <stop
                    offset="100%"
                    stopColor="#C65A24"
                    stopOpacity={0}
                  />
                </linearGradient>
              </defs>

              <CartesianGrid
                stroke="#8A8580"
                strokeOpacity={0.12}
                vertical={false}
              />

              <XAxis
                dataKey="time"
                axisLine={false}
                tickLine={false}
                tick={{
                  fill: "#8A8580",
                  fontSize: 11,
                  fontFamily: "Montserrat Alternates, sans-serif",
                }}
              />

              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{
                  fill: "#8A8580",
                  fontSize: 11,
                  fontFamily: "Montserrat Alternates, sans-serif",
                }}
              />

              <Tooltip
                contentStyle={{
                  background: "#1A1A1A",
                  border: "1px solid #8A8580",
                  borderRadius: "10px",
                  color: "#FFFFFF",
                  fontFamily: "Montserrat Alternates, sans-serif",
                }}
              />

              <Area
                type="monotone"
                dataKey="events"
                stroke="#C65A24"
                strokeWidth={2}
                fill="url(#darkOpsActivity)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Lower Information */}
      <div className="grid gap-5 border-t border-[#8A8580]/20 p-5 md:grid-cols-2">

        {/* Recent Activity */}
        <div>
          <p
            className="text-xs uppercase tracking-[0.15em] text-[#8A8580]"
            style={montserrat}
          >
            Recent Activity
          </p>

          <div className="mt-4 space-y-3">
            <div
              className="flex justify-between text-sm"
              style={montserrat}
            >
              <span className="text-[#1A1A1A] dark:text-white">
                Suspicious login detected
              </span>

              <span className="text-[#8A8580]">
                4m
              </span>
            </div>

            <div
              className="flex justify-between text-sm"
              style={montserrat}
            >
              <span className="text-[#1A1A1A] dark:text-white">
                Asset vulnerability recorded
              </span>

              <span className="text-[#8A8580]">
                18m
              </span>
            </div>

            <div
              className="flex justify-between text-sm"
              style={montserrat}
            >
              <span className="text-[#1A1A1A] dark:text-white">
                Incident status updated
              </span>

              <span className="text-[#8A8580]">
                32m
              </span>
            </div>
          </div>
        </div>

        {/* Protection Status */}
        <div>
          <p
            className="text-xs uppercase tracking-[0.15em] text-[#8A8580]"
            style={montserrat}
          >
            Protection Status
          </p>

          <div className="mt-4 space-y-3">
            <div
              className="flex items-center justify-between text-sm"
              style={montserrat}
            >
              <span className="text-[#1A1A1A] dark:text-white">
                Applications
              </span>

              <span className="text-green-500">
                17 / 18
              </span>
            </div>

            <div
              className="flex items-center justify-between text-sm"
              style={montserrat}
            >
              <span className="text-[#1A1A1A] dark:text-white">
                Assets
              </span>

              <span className="text-green-500">
                42 / 42
              </span>
            </div>

            <div
              className="flex items-center justify-between text-sm"
              style={montserrat}
            >
              <span className="text-[#1A1A1A] dark:text-white">
                Critical incidents
              </span>

              <span className="text-[#C65A24]">
                1 open
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

export default DashboardPreview;
