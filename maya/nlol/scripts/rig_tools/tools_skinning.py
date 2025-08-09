from maya import cmds


def select_skinned_joints():
    my_sel = cmds.ls(selection=True)
    skin_cluster_joints = cmds.skinCluster(my_sel[0], query=True, influence=True)
    cmds.select(skin_cluster_joints)
    print(skin_cluster_joints)


def get_skin_clusters():
    my_sel = cmds.ls(selection=True)
    history = cmds.listHistory(my_sel[0])
    skin_clusters = cmds.ls(history, type="skinCluster")
    print(skin_clusters)
