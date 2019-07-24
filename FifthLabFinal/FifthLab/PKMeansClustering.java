import java.util.concurrent.*;
import java.util.*;

public class PKMeansClustering {
	private int[] cluster;
	private ArrayList<double[]> u;
	private ArrayList<Node> points;

	public PKMeansClustering(int cutoff, Graph g, int k, int q) {
		points = g.getNodes();
		u = new ArrayList<double[]>();
		ForkJoinPool pool = new ForkJoinPool();
		this.points = points;
		cluster = new int[points.size()];
		initializeCentroids(k);

		for(int i=0;i<q;i++) {
			pool.invoke(new PSetClustering(cutoff, points, cluster, u, 0, points.size() - 1));
			pool.invoke(new PUpdateCentroid(cutoff, points, cluster, u, 0, u.size() - 1));
		}
	}

	public void initializeCentroids(int k) {
        long max = Integer.MIN_VALUE;
        Node toAdd = null;
        ArrayList<Node> nodeList = new ArrayList<Node>(points);
        Collections.sort(nodeList);
        for(int i=0;i<k;i++){
            u.add(nodeList.get(0).getCoords());
            nodeList.remove(nodeList.get(0));
        }
	}

	public int[] getClustering() {
		return cluster;
	}

	public ArrayList<double[]> getCentroids() {
		return u;
	}
}