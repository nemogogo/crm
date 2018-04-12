
perm_dic= {

    #'crm_table_index': ['table_index', 'GET', [], {'source':'qq'}, ],  # 可以查看audit APP里所有数据库表
    'audit_table_list': ['table_detail', 'GET', [], {}],  # 可以查看每张表里所有的数据
    'audit_table_list_view': ['table_change', 'GET', [], {}],  # 可以访问表里每条数据的修改页
    'audit_table_list_change': ['table_change', 'POST', [], {}],  # 可以对表里的每条数据进行修改
    'audit_table_obj_add_view': ['table_add', 'GET', [], {}],  # 可以访问数据增加页
    'audit_table_obj_add': ['table_add', 'POST', [], {}],  # 可以创建表里的数据

}



