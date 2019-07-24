import java.lang.String;
import java.lang.Math;
import java.util.*;
import java.io.*;
import org.apache.commons.math3.util.FastMath;

public class SerialKMeans {
	private ArrayList<Cluster> clusters;
	double RRR = 6378.388;

	public SerialKMeans(Graph g, int k, int q) {
        this.initializeClusters(g, k); // inizializzazione dei centroidi alle contee con il più alto numero di abitanti
        for(int i=0; i<q; i++) {
            this.eraseClusters();
            for(Node node: g.getNodes()) { //assegno ogni nodo al cluster più vicino
                this.insertNode(node); //inserisce il nodo corrente nel cluster il cui centroide è più vicino
            }
            for(Cluster c: clusters) {
                c.computeNewCentroid();
            }            
        }
	}

	private void initializeClusters(Graph g, int k) {
		clusters = new ArrayList<Cluster>();
		Cluster c = new Cluster();
        Graph temp = new Graph(g);
        ArrayList<Node> nodeList = temp.getNodes();
        Collections.sort(nodeList);
        for(int i=0;i<k;i++){
            c = new Cluster();
            c.setCentroid(nodeList.get(0).getCoords());
            nodeList.remove(nodeList.get(0));
            clusters.add(c);
        }
	}

	private void eraseClusters() {
        for(Cluster j: clusters) {
            j.eraseCluster();
        }
    }

    private void insertNode(Node n) {
        double min = Double.MAX_VALUE;
        double dist;
        Cluster toAdd = new Cluster();
        for(Cluster clust: clusters) {
            dist = this.calcDist(n.getCoords(), clust.getCentroid());
            if(dist < min) {
                min = dist;
                toAdd = clust;
            }
        }
        toAdd.addNode(n);
    }

    private int calcDist(double[] point1, double[] point2) {
        double x1 = convertToRadiant(point1[0]), x2 = convertToRadiant(point2[0]), y1 = convertToRadiant(point1[1]), y2 = convertToRadiant(point2[1]);
        double q1 = FastMath.cos(y1 - y2);
        double q2 = FastMath.cos(x1 - x2);
        double q3 = FastMath.cos(x1 + x2);
        return (int)(RRR * FastMath.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0);
    } 

    private double convertToRadiant(double value) {
        int deg = (int)value;
        double min = value - deg;
        return FastMath.PI * (deg + 5.0 * min / 3.0) / 180.0;
    }

    public ArrayList<Cluster> getClustering() {
    	return clusters;
    }
}