def create(root):
    a=raw_input('enter a key:');
    if a is '#':
        root=None;
    else:
        root=node(k=a);
        root.left=create(root.left);
        root.right=create(root.right);
    return root;

