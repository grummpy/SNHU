import java.util.*;

public class AdjacencyMatrixGraph extends DirectedGraph {
   protected ArrayList<Vertex> vertices = new ArrayList<>();

   // If matrixRows[X][Y] is true, then an edge exists from vertices[X] to
   // vertices[Y]
   protected ArrayList<ArrayList<Boolean>> matrixRows = new ArrayList<>();

   // Creates and adds a new vertex to the graph, provided a vertex with the
   // same label doesn't already exist in the graph. Returns the new vertex on
   // success, null on failure.
   @Override
   public Vertex addVertex(String newVertexLabel) {
      if (getVertex(newVertexLabel) != null) {
         return null;
      }

      Vertex newVertex = new Vertex(newVertexLabel);
      vertices.add(newVertex);

      for (ArrayList<Boolean> row : matrixRows) {
         row.add(false);
      }
      matrixRows.add(new ArrayList<>(Collections.nCopies(vertices.size(), false)));
      return newVertex;
   }

   // Adds a directed edge from the first to the second vertex. If the edge
   // already exists in the graph, no change is made and false is returned.
   // Otherwise the new edge is added and true is returned.
   @Override
   public boolean addDirectedEdge(Vertex fromVertex, Vertex toVertex) {
      int fromIndex = vertices.indexOf(fromVertex);
      int toIndex = vertices.indexOf(toVertex);
      if (fromIndex < 0 || toIndex < 0 || matrixRows.get(fromIndex).get(toIndex)) {
         return false;
      }

      matrixRows.get(fromIndex).set(toIndex, true);
      return true;
   }

   // Returns an ArrayList of edges with the specified fromVertex.
   @Override
   public ArrayList<Edge> getEdgesFrom(Vertex fromVertex) {
      ArrayList<Edge> edges = new ArrayList<>();
      int fromIndex = vertices.indexOf(fromVertex);
      if (fromIndex < 0) {
         return edges;
      }

      for (int toIndex = 0; toIndex < vertices.size(); ++toIndex) {
         if (matrixRows.get(fromIndex).get(toIndex)) {
            edges.add(new Edge(fromVertex, vertices.get(toIndex)));
         }
      }
      return edges;
   }

   // Returns an ArrayList of edges with the specified toVertex.
   @Override
   public ArrayList<Edge> getEdgesTo(Vertex toVertex) {
      ArrayList<Edge> edges = new ArrayList<>();
      int toIndex = vertices.indexOf(toVertex);
      if (toIndex < 0) {
         return edges;
      }

      for (int fromIndex = 0; fromIndex < vertices.size(); ++fromIndex) {
         if (matrixRows.get(fromIndex).get(toIndex)) {
            edges.add(new Edge(vertices.get(fromIndex), toVertex));
         }
      }
      return edges;
   }

   // Returns a vertex with a matching label, or null if no such vertex
   // exists
   @Override
   public Vertex getVertex(String vertexLabel) {
      for (Vertex vertex : vertices) {
         if (Objects.equals(vertex.getLabel(), vertexLabel)) {
            return vertex;
         }
      }
      return null;
   }

   // Returns true if this graph has an edge from fromVertex to toVertex
   @Override
   public boolean hasEdge(Vertex fromVertex, Vertex toVertex) {
      int fromIndex = vertices.indexOf(fromVertex);
      int toIndex = vertices.indexOf(toVertex);
      return fromIndex >= 0 && toIndex >= 0
            && matrixRows.get(fromIndex).get(toIndex);
   }
}
