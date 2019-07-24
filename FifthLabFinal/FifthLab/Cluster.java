import java.util.ArrayList;
import java.lang.String;

public class Cluster{
	private ArrayList<Node> nodes;
	private double[] centroid;

	public Cluster(){
		nodes = new ArrayList<>();
	}

	public ArrayList<Node> getNodes() {
        return nodes;
    }

    public void eraseCluster() {
    	nodes = new ArrayList<>();
    }

	public void addNode(Node node){
		nodes.add(node);
	}

	public void setCentroid(double[] c){
		centroid = c;
	}

	public void computeNewCentroid(){
		double sumX = 0;
		double sumY = 0;
		for(int i=0; i<nodes.size(); i++){
			sumX += nodes.get(i).getCoordX();
			sumY += nodes.get(i).getCoordY();
		}
		double[] newCentroid = new double[]{sumX/nodes.size(), sumY/nodes.size()};
		setCentroid(newCentroid);
	}

	public double[] getCentroid(){
		return centroid;
	}

	public String toString() {
        String out = "{ 'nodes': ";
        for (Node n: nodes) {
            out += n.toString() + ",";
        }
        out += " 'centroid: ' [" + Double.toString(centroid[0]) + ", " + Double.toString(centroid[1]) + "]}";
        return out;
    }
}