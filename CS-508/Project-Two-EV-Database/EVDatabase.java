import java.io.BufferedReader;
import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** In-memory EV database optimized for repeated searches by state. */
public final class EVDatabase {
    private static final int EXPECTED_COLUMNS = 10;

    private final ArrayList<EVRecord> records = new ArrayList<>();
    private final HashMap<String, ArrayList<EVRecord>> recordsByState = new HashMap<>();

    public static EVDatabase load(Path csvPath) throws IOException {
        EVDatabase database = new EVDatabase();
        try (BufferedReader reader = Files.newBufferedReader(csvPath, StandardCharsets.UTF_8)) {
            String line = reader.readLine(); // Header
            if (line == null) {
                throw new IOException("CSV file is empty: " + csvPath);
            }

            int lineNumber = 1;
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                if (line.trim().isEmpty()) {
                    continue;
                }
                List<String> columns = parseCsvLine(line);
                if (columns.size() != EXPECTED_COLUMNS) {
                    throw new IOException("Expected " + EXPECTED_COLUMNS + " columns at line "
                            + lineNumber + " but found " + columns.size());
                }
                database.add(parseRecord(columns, lineNumber));
            }
        }
        return database;
    }

    private static EVRecord parseRecord(List<String> c, int lineNumber) throws IOException {
        try {
            return new EVRecord(c.get(0), c.get(1), c.get(2), c.get(3),
                    Integer.parseInt(c.get(4)), Integer.parseInt(c.get(5)),
                    Integer.parseInt(c.get(6)), Integer.parseInt(c.get(7)),
                    Integer.parseInt(c.get(8)), Double.parseDouble(c.get(9)));
        } catch (NumberFormatException ex) {
            throw new IOException("Invalid numeric value at CSV line " + lineNumber, ex);
        }
    }

    /** Parses quoted commas and doubled quote characters without external libraries. */
    static List<String> parseCsvLine(String line) {
        ArrayList<String> fields = new ArrayList<>();
        StringBuilder field = new StringBuilder();
        boolean quoted = false;
        for (int i = 0; i < line.length(); i++) {
            char ch = line.charAt(i);
            if (ch == '"') {
                if (quoted && i + 1 < line.length() && line.charAt(i + 1) == '"') {
                    field.append('"');
                    i++;
                } else {
                    quoted = !quoted;
                }
            } else if (ch == ',' && !quoted) {
                fields.add(field.toString().trim());
                field.setLength(0);
            } else {
                field.append(ch);
            }
        }
        fields.add(field.toString().trim());
        return fields;
    }

    private void add(EVRecord record) {
        records.add(record);
        String key = normalizeState(record.getState());
        recordsByState.computeIfAbsent(key, ignored -> new ArrayList<>()).add(record);
    }

    private static String normalizeState(String state) {
        return state == null ? "" : state.trim().toUpperCase(Locale.ROOT);
    }

    /** Returns matching records in current database order. */
    public List<EVRecord> searchByState(String state) {
        ArrayList<EVRecord> matches = recordsByState.get(normalizeState(state));
        return matches == null ? new ArrayList<>() : new ArrayList<>(matches);
    }

    /** Sorts the database in place by EV percentage, highest first. */
    public void sortByPercentEV() {
        records.sort(Comparator.comparingDouble(EVRecord::getPercentEV).reversed());
        rebuildStateIndex();
    }

    private void rebuildStateIndex() {
        recordsByState.clear();
        for (EVRecord record : records) {
            recordsByState.computeIfAbsent(normalizeState(record.getState()),
                    ignored -> new ArrayList<>()).add(record);
        }
    }

    /** Calculates the required statistics in one pass over the data. */
    public Statistics calculateStatistics() {
        if (records.isEmpty()) {
            return new Statistics(0.0, 0L, "N/A", 0.0);
        }

        double percentageSum = 0.0;
        long totalEVs = 0L;
        HashMap<String, StateTotals> stateTotals = new HashMap<>();
        for (EVRecord record : records) {
            percentageSum += record.getPercentEV();
            totalEVs += (long) record.getBatteryElectricVehicles()
                    + record.getPlugInHybridElectricVehicles();
            String state = normalizeState(record.getState());
            if (!state.isEmpty()) {
                StateTotals totals = stateTotals.computeIfAbsent(state, ignored -> new StateTotals());
                totals.evCount += record.getElectricVehicleTotal();
                totals.vehicleCount += record.getTotalVehicles();
            }
        }

        String bestState = "N/A";
        double bestPercentage = -1.0;
        for (Map.Entry<String, StateTotals> entry : stateTotals.entrySet()) {
            StateTotals totals = entry.getValue();
            if (totals.vehicleCount == 0) {
                continue;
            }
            double percentage = 100.0 * totals.evCount / totals.vehicleCount;
            if (percentage > bestPercentage
                    || (percentage == bestPercentage && entry.getKey().compareTo(bestState) < 0)) {
                bestState = entry.getKey();
                bestPercentage = percentage;
            }
        }
        return new Statistics(percentageSum / records.size(), totalEVs,
                bestState, Math.max(0.0, bestPercentage));
    }

    /** Prints summary statistics in a user-friendly format. */
    public void generateStatistics() {
        generateStatistics(System.out);
    }

    public void generateStatistics(PrintStream output) {
        Statistics stats = calculateStatistics();
        output.printf("Average percentage of EVs: %.4f%%%n", stats.getAveragePercentEV());
        output.printf("Total number of EVs (BEVs + PHEVs): %,d%n", stats.getTotalEVs());
        output.printf("State with highest aggregate EV percentage: %s (%.4f%%)%n",
                stats.getHighestPercentState(), stats.getHighestStatePercentEV());
    }

    public int size() { return records.size(); }

    /** Returns a defensive copy so callers cannot mutate database storage. */
    public List<EVRecord> getRecords() { return new ArrayList<>(records); }

    private static final class StateTotals {
        long evCount;
        long vehicleCount;
    }

    public static final class Statistics {
        private final double averagePercentEV;
        private final long totalEVs;
        private final String highestPercentState;
        private final double highestStatePercentEV;

        Statistics(double averagePercentEV, long totalEVs,
                   String highestPercentState, double highestStatePercentEV) {
            this.averagePercentEV = averagePercentEV;
            this.totalEVs = totalEVs;
            this.highestPercentState = highestPercentState;
            this.highestStatePercentEV = highestStatePercentEV;
        }

        public double getAveragePercentEV() { return averagePercentEV; }
        public long getTotalEVs() { return totalEVs; }
        public String getHighestPercentState() { return highestPercentState; }
        public double getHighestStatePercentEV() { return highestStatePercentEV; }
    }
}
