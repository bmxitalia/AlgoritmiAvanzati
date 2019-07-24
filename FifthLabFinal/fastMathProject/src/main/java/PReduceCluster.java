import org.apache.commons.math3.util.FastMath;

import java.util.*;
import java.util.concurrent.*;

public class PReduceCluster extends RecursiveTask<SumSize> {
	private ArrayList<Node> p;
	private int[] cluster;
	private int start;
	private int end;
	private int h;
	private int cutoff;

	public PReduceCluster(int cutoff, ArrayList<Node> p, int[] cluster, int start, int end, int h) {
		this.p = p;
		this.cluster = cluster;
		this.start = start;
		this.end = end;
		this.h = h;
		this.cutoff = cutoff;
	}

	private SumSize serialStuff(int index) {
		if(cluster[index] == h) {
			return new SumSize(p.get(index).getCoords(), 1);
		}else{
			return new SumSize(new double[]{0.0, 0.0}, 0);
		}
	}

	@Override
	protected SumSize compute() {
		if((end - start) <= cutoff) {
			SumSize s = new SumSize(new double[]{0.0, 0.0}, 0);
			for(int i=start; i<=end; i++) {
				s = s.summ(serialStuff(i));
			}
			return s;
		}else {
			PReduceCluster p1 = new PReduceCluster(cutoff, p, cluster, start, (int)FastMath.floor((start + end)/2), h);
			p1.fork();
			PReduceCluster p2 = new PReduceCluster(cutoff, p, cluster, (int)FastMath.floor((start + end)/2) + 1, end, h);
			return p2.compute().summ(p1.join());
		}
	}
}