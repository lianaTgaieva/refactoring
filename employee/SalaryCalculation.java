public class SalaryCalculation {
    private double baseSalary;
    private int hoursWorked;
    private int overtimeHours;
    private double taxRate;
    private double pensionRate;
    private double healthInsuranceRate;

    // Конструктор со всеми полями...

    public double calculateNet() {
        double gross = baseSalary + (overtimeHours * baseSalary / 160 * 1.5);
        double deductions = gross * (taxRate + pensionRate + healthInsuranceRate);
        return gross - deductions;
    }
}