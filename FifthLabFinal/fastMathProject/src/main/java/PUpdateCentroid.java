import java.util.concurrent.*;
import java.util.*;
import org.apache.commons.math3.util.FastMath;

public class PUpdateCentroid extends RecursiveAction {
	private ArrayList<Node> points;
	private int[] cluster;
	private ArrayList<double[]> u;
	private int start;
	private int end;
	private int cutoff;

	public PUpdateCentroid(int cutoff, ArrayList<Node> points, int[] cluster, ArrayList<double[]> u, int start, int end) {
		this.points = points;
		this.cluster = cluster;
		this.u = u;
		this.start = start;
		this.end = end;
		this.cutoff = cutoff;
	}

	private void serialStuff(int index) {
		ForkJoinPool pool = new ForkJoinPool();
		SumSize sz = pool.invoke(new PReduceCluster(cutoff, points, cluster, 0, cluster.length - 1, index));
		double[] temp = sz.getSum();
		u.set(index, new double[]{temp[0] / sz.getSize(), temp[1] / sz.getSize()});
	}

	protected void compute() {
		if((end - start) <= cutoff) {
			for(int i=start; i<=end; i++) {
				serialStuff(i);
			}
		}else{
			invokeAll(new PUpdateCentroid(cutoff, points, cluster, u, start, (int)FastMath.floor((start + end)/2)),
				new PUpdateCentroid(cutoff, points, cluster, u, (int)FastMath.floor((start + end)/2) + 1, end));
		}
	}
}