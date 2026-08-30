import java.util.*;

public class AdjacencyListGraph extends DirectedGraph {
   protected ArrayList<AdjacencyListVertex> vertices = new ArrayList<>();

   // Creates and adds a new vertex to the graph, provided a vertex with the
   // same label doesn't already exist in the graph. Returns the new vertex on
   // success, null on failure.
   @Override
   public Vertex addVertex(String newVertexLabel) {
      if (getVertex(newVertexLabel) != null) {
         return null;
      }

      AdjacencyListVertex newVertex = new AdjacencyListVertex(newVertexLabel);
      vertices.add(newVertex);
      return newVertex;
   }

   // Adds a directed edge from the first to the second vertex. If the edge
   // already exists in the graph, no change is made and false is returned.
   // Otherwise the new edge is added and true is returned.
   @Override
   public boolean addDirectedEdge(Vertex fromVertex, Vertex toVertex) {
      if (!vertices.contains(fromVertex) || !vertices.contains(toVertex)
            || hasEdge(fromVertex, toVertex)) {
         return false;
      }

      ((AdjacencyListVertex) fromVertex).adjacent.add(toVertex);
      return true;
   }

   // Returns an ArrayList of edges with the specified fromVertex.
   @Override
   public ArrayList<Edge> getEdgesFrom(Vertex fromVertex) {
      ArrayList<Edge> edges = new ArrayList<>();
      if (!vertices.contains(fromVertex)) {
         return edges;
      }

      for (Vertex toVertex : ((AdjacencyListVertex) fromVertex).adjacent) {
         edges.add(new Edge(fromVertex, toVertex));
      }
      return edges;
   }

   // Returns an ArrayList of edges with the specified toVertex.
   @Override
   public ArrayList<Edge> getEdgesTo(Vertex toVertex) {
      ArrayList<Edge> edges = new ArrayList<>();
      if (!vertices.contains(toVertex)) {
         return edges;
      }

      for (AdjacencyListVertex fromVertex : vertices) {
         if (fromVertex.adjacent.contains(toVertex)) {
            edges.add(new Edge(fromVertex, toVertex));
         }
      }
      return edges;
   }

   // Returns a vertex with a matching label, or null if no such vertex
   // exists
   @Override
   public Vertex getVertex(String vertexLabel) {
      for (AdjacencyListVertex vertex : vertices) {
         if (Objects.equals(vertex.getLabel(), vertexLabel)) {
            return vertex;
         }
      }
      return null;
   }

   // Returns true if this graph has an edge from fromVertex to toVertex
   @Override
   public boolean hasEdge(Vertex fromVertex, Vertex toVertex) {
      return vertices.contains(fromVertex) && vertices.contains(toVertex)
            && ((AdjacencyListVertex) fromVertex).adjacent.contains(toVertex);
   }
}
