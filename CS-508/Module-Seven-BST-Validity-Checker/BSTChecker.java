import java.util.*;

public class BSTChecker {
   public static BSTNode checkBSTValidity(BSTNode rootNode) {
      Set<BSTNode> visitedNodes = new HashSet<>();
      return checkNode(rootNode, Long.MIN_VALUE, Long.MAX_VALUE,
            visitedNodes);
   }

   /**
    * Performs a preorder traversal while checking both BST key ranges and
    * whether the same node object has already been visited.
    */
   private static BSTNode checkNode(BSTNode node, long minKey, long maxKey,
                                    Set<BSTNode> visitedNodes) {
      // An empty child does not violate BST rules.
      if (node == null) {
         return null;
      }

      // A repeated node means that two parents share a child or a cycle exists.
      // add() returns false when this exact node object is already in the set.
      if (!visitedNodes.add(node)) {
         return node;
      }

      // Bounds are exclusive, so duplicate keys are also invalid.
      if (node.key <= minKey || node.key >= maxKey) {
         return node;
      }

      // Preorder checks the entire left subtree before the right subtree.
      BSTNode badNode = checkNode(node.left, minKey, node.key, visitedNodes);
      if (badNode != null) {
         return badNode;
      }

      return checkNode(node.right, node.key, maxKey, visitedNodes);
   }
}
