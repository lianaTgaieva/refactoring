public final class BankDetails {
    private final String account, name, routingNumber;

    public BankDetails(String account, String name, String routingNumber) {
        this.account = account; this.name = name; this.routingNumber = routingNumber;
    }

    public String getInfo() {
        return name + " " + account + " (" + routingNumber + ")";
    }
}