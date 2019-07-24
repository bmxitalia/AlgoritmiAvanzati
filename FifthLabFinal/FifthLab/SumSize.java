public class SumSize {
	private double[] sum;
	private int size;

	public SumSize(double[] sum, int size) {
		this.sum = sum;
		this.size = size;
	}

	public double[] getSum() {
		return sum;
	}

	public int getSize() {
		return size;
	}

	public SumSize summ(SumSize snd) {
		double[] sndSum = snd.getSum();
		int sndSize = snd.getSize();
		return new SumSize(new double[]{sum[0] + sndSum[0], sum[1] + sndSum[1]}, size + sndSize);
	}
}