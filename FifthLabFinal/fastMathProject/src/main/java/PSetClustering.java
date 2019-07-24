import java.util.concurrent.*;
import java.util.*;
import org.apache.commons.math3.util.FastMath;

public class PSetClustering extends RecursiveAction {
	private ArrayList<Node> points;
	private int[] cluster;
	private ArrayList<double[]> u;
	private int start;
	private int end;
	private int cutoff;

	public PSetClustering(int cutoff, ArrayList<Node> points, int[] cluster, ArrayList<double[]> u, int start, int end) {
		this.points = points;
		this.cluster = cluster;
		this.u = u;
		this.start = start;
		this.end = end;
		this.cutoff = cutoff;
	}

	private void serialStuff(int index) {
		int dist;
		int indexMin = 0;
		int min = Integer.MAX_VALUE;
		for(double[] arr: u) {
			dist = calcDist(points.get(index).getCoords(), arr);
			if(dist < min) {
				min = dist;
				indexMin = u.indexOf(arr);
			}
		}
		cluster[index] = indexMin;
	}

	protected void compute() {
		if((end - start) <= cutoff) {
			for(int i=start; i<=end; i++) {
				serialStuff(i);
			}
		}else {
			invokeAll(new PSetClustering(cutoff, points, cluster, u, start, (int)FastMath.floor((start + end)/2)),
				new PSetClustering(cutoff, points, cluster, u, (int)FastMath.floor((start + end)/2) + 1, end));
		}
	}

	public int calcDist(double[] point1, double[] point2) {
        double RRR = 6378.388;
        double x1 = convertToRadiant(point1[0]), x2 = convertToRadiant(point2[0]), y1 = convertToRadiant(point1[1]), y2 = convertToRadiant(point2[1]);
        double q1 = FastMath.cos(y1 - y2);
        double q2 = FastMath.cos(x1 - x2);
        double q3 = FastMath.cos(x1 + x2);
        return (int)(RRR * FastMath.acos(0.5 * ((1.0 + q1) * q2 - (1.0 - q1) * q3)) + 1.0);
    } 

    public double convertToRadiant(double value) {
        int deg = (int)value;
        double min = value - deg;
        return FastMath.PI * (deg + 5.0 * min / 3.0) / 180.0;
    }
}