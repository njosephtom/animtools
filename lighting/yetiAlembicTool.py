import maya.cmds as cmds

class AlembicRetargetTool:
    def __init__(self):
        self.window = "alembicRetargetWin"
        self.source_list = None
        self.target_list = None

    # ---------------- UI ---------------- #
    def show(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window)

        self.window = cmds.window(self.window, title="Alembic Retarget Tool", widthHeight=(450, 300))
        cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

        # SOURCE
        cmds.text(label="Source Groups (Animated Alembic)")
        self.source_list = cmds.textScrollList(height=100)
        cmds.rowLayout(numberOfColumns=3)
        cmds.button(label="Add Selected", c=self.add_source)
        cmds.button(label="Remove", c=self.remove_source)
        cmds.button(label="Clear", c=lambda *_: cmds.textScrollList(self.source_list, e=True, removeAll=True))
        cmds.setParent("..")

        # TARGET
        cmds.text(label="Target Groups (To Drive)")
        self.target_list = cmds.textScrollList(height=100)
        cmds.rowLayout(numberOfColumns=3)
        cmds.button(label="Add Selected", c=self.add_target)
        cmds.button(label="Remove", c=self.remove_target)
        cmds.button(label="Clear", c=lambda *_: cmds.textScrollList(self.target_list, e=True, removeAll=True))
        cmds.setParent("..")

        cmds.separator(height=10)
        cmds.button(label="Retarget Animation", height=40, command=self.retarget)
        cmds.showWindow(self.window)

    # ---------------- UI Helpers ---------------- #
    def add_source(self, *_):
        sel = cmds.ls(selection=True, long=True) or []
        existing = cmds.textScrollList(self.source_list, q=True, allItems=True) or []
        for s in sel:
            if s not in existing:
                cmds.textScrollList(self.source_list, e=True, append=s)

    def remove_source(self, *_):
        sel = cmds.textScrollList(self.source_list, q=True, selectItem=True) or []
        for s in sel:
            cmds.textScrollList(self.source_list, e=True, removeItem=s)

    def add_target(self, *_):
        sel = cmds.ls(selection=True, long=True) or []
        existing = cmds.textScrollList(self.target_list, q=True, allItems=True) or []
        for s in sel:
            if s not in existing:
                cmds.textScrollList(self.target_list, e=True, append=s)

    def remove_target(self, *_):
        sel = cmds.textScrollList(self.target_list, q=True, selectItem=True) or []
        for s in sel:
            cmds.textScrollList(self.target_list, e=True, removeItem=s)

    # ---------------- Core Helpers ---------------- #
    def collect_shapes(self, roots):
        """
        Recursively collect all mesh and nurbsCurve shapes under each root group.
        Fully ignores namespaces.
        """
        result = {}
        for root in roots or []:
            # Traverse all descendants + root itself
            all_transforms = cmds.listRelatives(root, allDescendents=True, fullPath=True) or []
            all_transforms.append(root)

            for obj in all_transforms:
                shapes = cmds.listRelatives(obj, shapes=True, fullPath=True) or []
                for s in shapes:
                    if cmds.nodeType(s) not in ["mesh", "nurbsCurve"]:
                        continue
                    parent = (cmds.listRelatives(s, parent=True, fullPath=True) or [None])[0]
                    if not parent:
                        continue
                    # Strip namespaces for matching
                    short_name = parent.split("|")[-1].split(":")[-1]
                    if short_name not in result:
                        result[short_name] = s
        return result

    def get_final_shape(self, shape):
        """Return visible (non-intermediate) shape"""
        if not cmds.getAttr(shape + ".intermediateObject"):
            return shape
        outputs = cmds.listConnections(shape, s=False, d=True, shapes=True) or []
        for o in outputs:
            if not cmds.getAttr(o + ".intermediateObject"):
                return o
        return shape

    def disconnect_incoming(self, plug):
        """Disconnect anything driving this plug"""
        connections = cmds.listConnections(plug, plugs=True, source=True, destination=False) or []
        for c in connections:
            try:
                cmds.disconnectAttr(c, plug)
            except:
                pass

    # ---------------- Connections ---------------- #
    def connect_mesh(self, src_shape, tgt_shape):
        try:
            src_shape = self.get_final_shape(src_shape)
            tgt_shape = self.get_final_shape(tgt_shape)
            self.disconnect_incoming(tgt_shape + ".inMesh")
            cmds.connectAttr(src_shape + ".outMesh", tgt_shape + ".inMesh", force=True)
        except Exception as e:
            print(f"[Mesh Connect Failed] {src_shape} -> {tgt_shape} : {e}")

    def connect_curve(self, src_shape, tgt_shape):
        try:
            src_shape = self.get_final_shape(src_shape)
            tgt_shape = self.get_final_shape(tgt_shape)
            self.disconnect_incoming(tgt_shape + ".create")
            cmds.connectAttr(src_shape + ".local", tgt_shape + ".create", force=True)
        except Exception as e:
            print(f"[Curve Connect Failed] {src_shape} -> {tgt_shape} : {e}")

    # ---------------- Retarget ---------------- #
    def retarget(self, *_):
        source_roots = cmds.textScrollList(self.source_list, q=True, allItems=True) or []
        target_roots = cmds.textScrollList(self.target_list, q=True, allItems=True) or []

        if not source_roots or not target_roots:
            cmds.warning("Add at least one source and one target group.")
            return

        print("Collecting source shapes...")
        src_shapes = self.collect_shapes(source_roots)
        print("Collecting target shapes...")
        tgt_shapes = self.collect_shapes(target_roots)

        matched = 0
        for name, tgt_shape in tgt_shapes.items():
            if name not in src_shapes:
                continue
            src_shape = src_shapes[name]
            src_type = cmds.nodeType(src_shape)
            tgt_type = cmds.nodeType(tgt_shape)
            if src_type != tgt_type:
                print(f"[Type Mismatch] {name}")
                continue
            if src_type == "mesh":
                self.connect_mesh(src_shape, tgt_shape)
                matched += 1
            elif src_type == "nurbsCurve":
                self.connect_curve(src_shape, tgt_shape)
                matched += 1

        print(f":white_check_mark: Retarget complete. Matched: {matched}")
        
        
win = AlembicRetargetTool()
win.show()        