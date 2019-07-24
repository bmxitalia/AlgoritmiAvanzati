import java.lang.String;

public class Node implements Comparable {
    private String code;
    private double[] coords;
    private long population;
    private String risk;
    
    public Node(String code, double[] coords, long population, String risk) {
        this.code = code;
        this.coords = coords;
        this.population = population;
        this.risk = risk;
    }

    public int compareTo(Object compareNode) {
        long comparePopulation = ((Node)compareNode).getPopulation();
        return (int)(comparePopulation - this.population);
    }

    public String getCode() {
        return code;
    }

    public double[] getCoords() {
        return coords;
    }

    public double getCoordX() {
        return coords[0];
    }

    public double getCoordY() {
        return coords[1];
    }
    
    public long getPopulation() {
        return population;
    }

    public String getRisk() {
        return risk;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public void setCoords(double[] coords) {
        this.coords = coords;
    }

    public void setCoordX(double x) {
        coords[0] = x;
    }

    public void setCoordY(double y) {
        coords[1] = y;
    }

    public void setPopulation(long population) {
        this.population = population;
    }

    public void setRisk(String risk) {
        this.risk = risk;
    }

    public String toString() {
        return "'"+code+"'";
    }
}