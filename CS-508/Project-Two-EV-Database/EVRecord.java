import java.util.Objects;

/** Immutable representation of one electric-vehicle registration record. */
public final class EVRecord {
    private final String date;
    private final String county;
    private final String state;
    private final String vehiclePrimaryUse;
    private final int batteryElectricVehicles;
    private final int plugInHybridElectricVehicles;
    private final int electricVehicleTotal;
    private final int nonElectricVehicleTotal;
    private final int totalVehicles;
    private final double percentEV;

    public EVRecord(String date, String county, String state, String vehiclePrimaryUse,
                    int batteryElectricVehicles, int plugInHybridElectricVehicles,
                    int electricVehicleTotal, int nonElectricVehicleTotal,
                    int totalVehicles, double percentEV) {
        this.date = Objects.requireNonNull(date, "date");
        this.county = Objects.requireNonNull(county, "county");
        this.state = Objects.requireNonNull(state, "state");
        this.vehiclePrimaryUse = Objects.requireNonNull(vehiclePrimaryUse, "vehiclePrimaryUse");
        this.batteryElectricVehicles = batteryElectricVehicles;
        this.plugInHybridElectricVehicles = plugInHybridElectricVehicles;
        this.electricVehicleTotal = electricVehicleTotal;
        this.nonElectricVehicleTotal = nonElectricVehicleTotal;
        this.totalVehicles = totalVehicles;
        this.percentEV = percentEV;
    }

    public String getDate() { return date; }
    public String getCounty() { return county; }
    public String getState() { return state; }
    public String getVehiclePrimaryUse() { return vehiclePrimaryUse; }
    public int getBatteryElectricVehicles() { return batteryElectricVehicles; }
    public int getPlugInHybridElectricVehicles() { return plugInHybridElectricVehicles; }
    public int getElectricVehicleTotal() { return electricVehicleTotal; }
    public int getNonElectricVehicleTotal() { return nonElectricVehicleTotal; }
    public int getTotalVehicles() { return totalVehicles; }
    public double getPercentEV() { return percentEV; }

    @Override
    public String toString() {
        return String.format("%s, %s, %s, %s, EV total=%d, percentEV=%.2f%%",
                date, county, state, vehiclePrimaryUse, electricVehicleTotal, percentEV);
    }
}
