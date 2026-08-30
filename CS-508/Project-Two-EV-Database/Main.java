import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

/** Command-line entry point for the EV database. */
public final class Main {
    private Main() { }

    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.err.println("Usage: java Main <csv-file> [state]");
            return;
        }

        Path csvPath = Paths.get(args[0]);
        String state = args.length > 1 ? args[1] : "WA";

        long loadStart = System.nanoTime();
        EVDatabase database = EVDatabase.load(csvPath);
        long loadNanos = System.nanoTime() - loadStart;

        long searchStart = System.nanoTime();
        List<EVRecord> matches = database.searchByState(state);
        long searchNanos = System.nanoTime() - searchStart;

        long sortStart = System.nanoTime();
        database.sortByPercentEV();
        long sortNanos = System.nanoTime() - sortStart;

        System.out.printf("Loaded %,d records in %.3f ms%n", database.size(), loadNanos / 1_000_000.0);
        System.out.printf("Found %,d records for %s in %.3f ms%n",
                matches.size(), state.toUpperCase(), searchNanos / 1_000_000.0);
        System.out.printf("Sorted by percentEV descending in %.3f ms%n", sortNanos / 1_000_000.0);
        database.generateStatistics();
    }
}
