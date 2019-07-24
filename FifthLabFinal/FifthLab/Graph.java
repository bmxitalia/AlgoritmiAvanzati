import java.util.ArrayList;
import java.util.stream.Collectors;

public class Graph {
    private ArrayList<Node> nodes;

    public Graph() {
        nodes = new ArrayList<>();
    }

    public Graph(Graph g) {
        nodes = new ArrayList<>(g.getNodes());
    }

    public void add(Node n) {
        nodes.add(n);
    }

    public void remove(Node n) {
        nodes.remove(n);
    }

    public ArrayList<Node> getNodes() {
        return nodes;
    }

    public void setNodes(ArrayList<Node> nodes) {
        this.nodes = nodes;
    }

    public int getDim() {
        return nodes.size();
    }

    public ArrayList<Node> getNodesByPopulation(int limit) {
        ArrayList<Node> tmp = new ArrayList<Node>();

        for(Node n: this.nodes) {
            if (n.getPopulation() >= limit) {
                tmp.add(n);
            }
        }
        return tmp;
    }

    public String toString() {
        String out = "{";
        for (Node n: nodes) {
            out += n.toString() + ",";
        }
        out += "}";
        return out;
    }
}