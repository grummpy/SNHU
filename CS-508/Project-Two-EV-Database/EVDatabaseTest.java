import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.List;

/** Dependency-free correctness and performance test harness. */
public final class EVDatabaseTest {
    private EVDatabaseTest() { }

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            throw new IllegalArgumentException("Usage: java EVDatabaseTest <csv-file>");
        }

        testCsvParser();
        Path csvPath = Paths.get(args[0]);
        EVDatabase database = EVDatabase.load(csvPath);
        check(database.size() == 24_449, "Expected 24,449 records");
        check(database.searchByState("wa").size() == 7_410, "Case-insensitive WA search");
        check(database.searchByState("ZZ").isEmpty(), "Unknown state returns empty list");

        database.sortByPercentEV();
        List<EVRecord> sorted = database.getRecords();
        boolean descending = true;
        for (int i = 1; i < sorted.size(); i++) {
            if (sorted.get(i - 1).getPercentEV() < sorted.get(i).getPercentEV()) {
                descending = false;
                break;
            }
        }
        check(descending, "Descending sort across all records");

        EVDatabase.Statistics stats = database.calculateStatistics();
        check(Math.abs(stats.getAveragePercentEV() - 4.4054623911) < 0.000001,
                "Average EV percentage");
        check(stats.getTotalEVs() == 7_974_224L, "Total EV count");
        check("PR".equals(stats.getHighestPercentState()), "Highest aggregate EV state");
        check(Math.abs(stats.getHighestStatePercentEV() - 40.7079646018) < 0.000001,
                "Highest state EV percentage");

        benchmarkSearch(database);
        System.out.println("ALL TESTS PASSED");
    }

    private static void testCsvParser() {
        List<String> parsed = EVDatabase.parseCsvLine("a,\"b,c\",\"d\"\"e\"");
        check(parsed.equals(Arrays.asList("a", "b,c", "d\"e")), "Quoted CSV parsing");
    }

    private static void benchmarkSearch(EVDatabase database) {
        for (int i = 0; i < 2_000; i++) {
            database.searchByState((i & 1) == 0 ? "WA" : "OR");
        }
        long start = System.nanoTime();
        int resultCount = 0;
        int iterations = 10_000;
        for (int i = 0; i < iterations; i++) {
            resultCount += database.searchByState((i & 1) == 0 ? "WA" : "OR").size();
        }
        long elapsed = System.nanoTime() - start;
        System.out.printf("Indexed state-search benchmark: %,d searches, %,d returned records, %.3f ms%n",
                iterations, resultCount, elapsed / 1_000_000.0);
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError("FAILED: " + message);
        }
        System.out.println("PASS: " + message);
    }
}
