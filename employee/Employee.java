public class Employee {
    private String name;
    private String department;
    private SalaryCalculation salary;
    private BankDetails bankDetails;
    private Address address;

    public void sendPayslip() {
        double net = salary.calculateNet();
        // Мы не лезем внутрь address.getCity(), мы просим объект предоставить формат
        String addr = address.format(); 
        String bankInfo = bankDetails.getInfo();

        PostalService.send(addr, "Payslip: " + net);
        BankService.transfer(bankInfo, net);
        Logger.log(name + " paid " + net + " to " + bankInfo);
    }
}