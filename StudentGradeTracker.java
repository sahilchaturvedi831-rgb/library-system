import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Scanner;

public class StudentGradeTracker {

    private static class Student {
        String name;
        List<Integer> grades;

        Student(String name) {
            this.name = name;
            this.grades = new ArrayList<>();
        }

        double getAverage() {
            if (grades.isEmpty())
                return 0.0;
            int sum = 0;
            for (int g : grades)
                sum += g;
            return sum / (double) grades.size();
        }

        int getHighest() {
            if (grades.isEmpty())
                return Integer.MIN_VALUE;
            return Collections.max(grades);
        }

        int getLowest() {
            if (grades.isEmpty())
                return Integer.MAX_VALUE;
            return Collections.min(grades);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.println("=== Student Grade Tracker ===");

        int studentCount = readIntInRange(sc, "Enter number of students: ", 1, 1000);

        List<Student> students = new ArrayList<>();

        for (int i = 0; i < studentCount; i++) {
            System.out.println();
            System.out.println("--- Student " + (i + 1) + " ---");

            System.out.print("Enter student name: ");
            String name = sc.nextLine().trim();
            while (name.isEmpty()) {
                System.out.print("Name cannot be empty. Enter student name: ");
                name = sc.nextLine().trim();
            }

            int gradeCount = readIntInRange(sc, "Enter number of grades for " + name + ": ", 1, 1000);
            Student st = new Student(name);

            for (int j = 0; j < gradeCount; j++) {
                int grade = readIntInRange(sc, "Enter grade " + (j + 1) + " (0-100): ", 0, 100);
                st.grades.add(grade);
            }

            students.add(st);
        }

        // Compute global highest/lowest across all grades
        Integer globalHighest = null;
        Integer globalLowest = null;

        System.out.println();
        System.out.println("=== Summary Report ===");

        for (Student st : students) {
            // Update global
            for (int g : st.grades) {
                if (globalHighest == null || g > globalHighest)
                    globalHighest = g;
                if (globalLowest == null || g < globalLowest)
                    globalLowest = g;
            }

            System.out.println("Student: " + st.name);
            System.out.print("Grades: ");
            for (int k = 0; k < st.grades.size(); k++) {
                System.out.print(st.grades.get(k));
                if (k < st.grades.size() - 1)
                    System.out.print(", ");
            }
            System.out.println();

            System.out.printf("Average: %.2f%n", st.getAverage());
            System.out.println("Highest grade (student): " + st.getHighest());
            System.out.println("Lowest grade (student): " + st.getLowest());
            System.out.println();
        }

        System.out.println("=== Overall (All Students) ===");
        System.out.println("Highest score: " + globalHighest);
        System.out.println("Lowest score: " + globalLowest);

        sc.close();
    }

    private static int readIntInRange(Scanner sc, String prompt, int min, int max) {
        while (true) {
            System.out.print(prompt);
            String line = sc.nextLine().trim();
            try {
                int value = Integer.parseInt(line);
                if (value < min || value > max) {
                    System.out.println("Invalid input. Enter a value between " + min + " and " + max + ".");
                    continue;
                }
                return value;
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter an integer.");
            }
        }
    }
}
