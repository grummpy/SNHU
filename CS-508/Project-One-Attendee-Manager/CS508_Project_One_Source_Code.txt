import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Cleans, sorts, and removes duplicate conference attendee names.
 *
 * This solution uses a custom resizable array and a custom merge sort.
 * It does not use Java collection classes or Java sorting utilities.
 */
public class ConferenceAttendeeManager {

    /** Simple custom resizable array for attendee names. */
    private static class NameArray {
        private String[] items;
        private int size;

        NameArray() {
            items = new String[16];
            size = 0;
        }

        void add(String name) {
            if (size == items.length) {
                grow();
            }
            items[size] = name;
            size++;
        }

        String get(int index) {
            if (index < 0 || index >= size) {
                throw new IndexOutOfBoundsException("Invalid index: " + index);
            }
            return items[index];
        }

        void set(int index, String value) {
            if (index < 0 || index >= size) {
                throw new IndexOutOfBoundsException("Invalid index: " + index);
            }
            items[index] = value;
        }

        int size() {
            return size;
        }

        private void grow() {
            String[] larger = new String[items.length * 2];
            for (int i = 0; i < size; i++) {
                larger[i] = items[i];
            }
            items = larger;
        }
    }

    public static void main(String[] args) {
        if (args.length < 3) {
            printUsage();
            return;
        }

        String inputFile = args[0];
        String outputFile = args[1];
        String duplicateFile = args[2];

        try {
            NameArray names = readAndCleanNames(inputFile);
            int originalCount = names.size();

            mergeSort(names);
            int uniqueCount = writeUniqueCsvAndDuplicateReport(
                    names, outputFile, duplicateFile);

            System.out.println("Processing complete.");
            System.out.println("Valid names read: " + originalCount);
            System.out.println("Unique names written: " + uniqueCount);
            System.out.println("Duplicate entries removed: "
                    + (originalCount - uniqueCount));
            System.out.println("Master CSV: " + outputFile);
            System.out.println("Duplicate report: " + duplicateFile);
        } catch (IOException exception) {
            System.err.println("File error: " + exception.getMessage());
        }
    }

    /** Reads one name per line, cleans it, and skips blank results. */
    private static NameArray readAndCleanNames(String inputFile)
            throws IOException {
        NameArray names = new NameArray();

        try (BufferedReader reader = new BufferedReader(
                new FileReader(inputFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                String cleaned = cleanName(line);
                if (!cleaned.isEmpty()) {
                    names.add(cleaned);
                }
            }
        }

        return names;
    }

    /**
     * Keeps letters, spaces, apostrophes, and hyphens; removes other
     * characters; collapses extra spaces; and applies name capitalization.
     */
    private static String cleanName(String rawName) {
        StringBuilder cleaned = new StringBuilder();
        boolean previousWasSpace = true;

        for (int i = 0; i < rawName.length(); i++) {
            char current = rawName.charAt(i);

            if (Character.isLetter(current)) {
                cleaned.append(Character.toLowerCase(current));
                previousWasSpace = false;
            } else if (current == '\'' || current == '-') {
                if (cleaned.length() > 0 && !previousWasSpace) {
                    cleaned.append(current);
                }
            } else if (Character.isWhitespace(current)) {
                if (cleaned.length() > 0 && !previousWasSpace) {
                    cleaned.append(' ');
                    previousWasSpace = true;
                }
            }
        }

        int length = cleaned.length();
        if (length > 0 && cleaned.charAt(length - 1) == ' ') {
            cleaned.deleteCharAt(length - 1);
        }

        boolean capitalizeNext = true;
        for (int i = 0; i < cleaned.length(); i++) {
            char current = cleaned.charAt(i);
            if (Character.isLetter(current)) {
                if (capitalizeNext) {
                    cleaned.setCharAt(i, Character.toUpperCase(current));
                }
                capitalizeNext = false;
            } else {
                capitalizeNext = current == ' ' || current == '-'
                        || current == '\'';
            }
        }

        return cleaned.toString();
    }

    /** Starts merge sort when there are at least two names. */
    private static void mergeSort(NameArray names) {
        if (names.size() < 2) {
            return;
        }

        String[] temporary = new String[names.size()];
        mergeSort(names, temporary, 0, names.size() - 1);
    }

    /** Recursively divides the array into smaller halves. */
    private static void mergeSort(NameArray names, String[] temporary,
            int left, int right) {
        if (left >= right) {
            return;
        }

        int middle = left + (right - left) / 2;
        mergeSort(names, temporary, left, middle);
        mergeSort(names, temporary, middle + 1, right);
        merge(names, temporary, left, middle, right);
    }

    /** Combines two sorted halves into one sorted section. */
    private static void merge(NameArray names, String[] temporary,
            int left, int middle, int right) {
        int first = left;
        int second = middle + 1;
        int output = left;

        while (first <= middle && second <= right) {
            if (names.get(first).compareToIgnoreCase(names.get(second)) <= 0) {
                temporary[output] = names.get(first);
                first++;
            } else {
                temporary[output] = names.get(second);
                second++;
            }
            output++;
        }

        while (first <= middle) {
            temporary[output] = names.get(first);
            first++;
            output++;
        }

        while (second <= right) {
            temporary[output] = names.get(second);
            second++;
            output++;
        }

        for (int i = left; i <= right; i++) {
            names.set(i, temporary[i]);
        }
    }

    /**
     * Writes the unique sorted list and a separate duplicate review file.
     * Because equal names are next to each other after sorting, only one
     * forward pass is needed.
     */
    private static int writeUniqueCsvAndDuplicateReport(NameArray names,
            String outputFile, String duplicateFile) throws IOException {
        int uniqueCount = 0;

        try (BufferedWriter output = new BufferedWriter(
                    new FileWriter(outputFile));
             BufferedWriter duplicates = new BufferedWriter(
                    new FileWriter(duplicateFile))) {

            output.write("Attendee Name");
            output.newLine();
            duplicates.write("Attendee Name,Total Occurrences");
            duplicates.newLine();

            int index = 0;
            while (index < names.size()) {
                String current = names.get(index);
                int occurrences = 1;
                index++;

                while (index < names.size()
                        && current.equalsIgnoreCase(names.get(index))) {
                    occurrences++;
                    index++;
                }

                output.write(csvValue(current));
                output.newLine();
                uniqueCount++;

                if (occurrences > 1) {
                    duplicates.write(csvValue(current));
                    duplicates.write("," + occurrences);
                    duplicates.newLine();
                }
            }
        }

        return uniqueCount;
    }

    /** Safely places a value into one CSV column. */
    private static String csvValue(String value) {
        String escaped = value.replace("\"", "\"\"");
        return "\"" + escaped + "\"";
    }

    private static void printUsage() {
        System.out.println("Usage:");
        System.out.println("java ConferenceAttendeeManager "
                + "<input.txt> <master.csv> <duplicates.csv>");
    }
}
