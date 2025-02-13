import matplotlib.pyplot as plt

class Lineage:
    
    def __init__(self, lin_id, lin_interval, n_cell):
        self.lin_id=lin_id
        self.lin_interval=lin_interval
        self.n_cell=n_cell

    def lineage_divide_cell(self,lin_id, lin_interval, t_div, ind_mother, ind_daughter_list, n_cell):
        # if current branch is not a list
        if type(lin_id)!=list:
            # then it has not sublineage
            if lin_id==ind_mother:
                # if the id of this branch is that of the dividing cell, implement the division
                # replace the id with a list of the two daughter cell ids
                lin_id=[ind_mother,ind_daughter_list]
                # replace the time of birth of cell <lin_id> with an interval
                # [t_birth_<lin_id>, [t_birth_daughter0, t_birth_daughter1]]
                lin_interval=[lin_interval,[t_div,t_div]]
                # and increase the cell count for the lineage
                n_cell=n_cell+1
        else:
            # if it is a list, it has a sublineage
            for i in range(0,2):
                # for each daughter sublineage, get the id and time interval data
                sub_lin_id = lin_id[1][i]
                sub_lin_interval = lin_interval[1][i]
                # and search for cell (and implement division when found) in sublineage
                (sub_lin_id,sub_lin_interval,n_cell) = self.lineage_divide_cell(sub_lin_id, sub_lin_interval, t_div, ind_mother, ind_daughter_list, n_cell)
                # and update sublineages in lineage data
                lin_id[1][i]=sub_lin_id
                lin_interval[1][i]=sub_lin_interval
    
        # return updated lineage data        
        return (lin_id,lin_interval,n_cell)

    def divide_cell(self, id_mother, id_daughter_list, t_divide):
        # id_mother: label of mother cell
        # id_daughter_cell_list: list of [daughter1_id, daughter2_id]
        # t_divide: time of division
        (self.lin_id,self.lin_interval,self.n_cell)=self.lineage_divide_cell(self.lin_id,self.lin_interval,t_divide,id_mother,id_daughter_list,self.n_cell)

    def get_sublineage_draw_data(self,lin_id,lin_interval,t_end,x_curr_branch,x_end_branch,line_list):
        # if current branch is not a list
        if type(lin_id)!=list:
            # then it has no sublineage, so we plot an end branch
            # set x position of current branch to that of the next end branch
            x_curr_branch=x_end_branch
            # plot line from time of birth to end time of lineage tree
#            plt.plot([x_curr_branch,x_curr_branch],[lin_interval,t_end],'-k')
            X=[x_curr_branch]
            T=[lin_interval,t_end]
            CID=lin_id
            line_list.append( [X,T,CID] )
#            plt.text(x_curr_branch, lin_interval, lin_id)
            # and increase the position of the next end branch 
            x_end_branch=x_end_branch+1
        else:
            # if it is a list, it has a sublineage
            x=[]
            for i in range(0,2):
                # for each daughter sublineage, get the id and time interval data
                sub_lin_id = lin_id[1][i]
                sub_lin_interval = lin_interval[1][i]
                # and draw sublineage sublineage
                (x_curr_branch,x_end_branch,line_list) = self.get_sublineage_draw_data(sub_lin_id, sub_lin_interval,t_end,x_curr_branch,x_end_branch,line_list)
                # for each sublineage, save the current branch x position
                x.append(x_curr_branch)
            # get the start of the time interval
            t0=lin_interval[0]
            CID=lin_id[0]
            # and the end            
            if type(lin_interval[1][0])!=list:
                t1=lin_interval[1][0]
#                cell_id=lin_id[1][0]
            else:
                t1=lin_interval[1][0][0]
            # plot horizontal line connected the two daughter branches
#            plt.plot([x[0],x[1]], [ t1,t1 ], '-k')
            X=[x[0],x[1]]
            T=[t1]
            line_list.append( [X,T,CID] )

            # and plot the mother branch
            x_curr_branch=(x[0]+x[1])/2.
#            plt.plot([x_curr_branch,x_curr_branch], [ t0,t1 ], '-k')
#            plt.text(x_curr_branch, t0, cell_id)
            X=[x_curr_branch]
            T=[t0,t1]
            line_list.append( [X,T,CID] )
    
        # return updated lineage data        
        return (x_curr_branch,x_end_branch,line_list)

    def get_lineage_draw_data(self, t_end):
        (x_curr,x_end,line_list)=self.get_sublineage_draw_data(self.lin_id,self.lin_interval,t_end,0,0,[])
        return( (x_end,line_list) )
        
    def draw_lineage(self,T_end,x_offset,show_cell_id=False,col='k'):
        (diagram_width, line_list)=self.get_lineage_draw_data(T_end)
    
        for l in line_list:
            X=l[0]
            T=l[1]
            CID=l[2]
            if len(T)==2:
                ## two timepoints T, so this is a vertical line
                # plot line
                plt.plot( [x_offset+X[0],x_offset+X[0]], T, '-'+col )
                if show_cell_id:
                    # print cell id
                    plt.text( x_offset+X[0], T[0], CID)
            if len(X)==2:
                ## two x positions, so this a horizontal line indicating division
                # plot line
                plt.plot( [x_offset+X[0],x_offset+X[1]], [T[0],T[0]], '-'+col )
        return(diagram_width)
        
#    def draw_lineage(self,lin_id, lin_interval,t_end,x_curr_branch,x_end_branch):
#        # if current branch is not a list
#        if type(lin_id)!=list:
#            # then it has not sublineage, so we plot an end branch
#            # set x position of current branch to that of the next end branch
#            x_curr_branch=x_end_branch
#            # plot line from time of birth to end time of lineage tree
#            plt.plot([x_curr_branch,x_curr_branch],[lin_interval,t_end],'-k')
#            # and increase the position of the next end branch 
#            x_end_branch=x_end_branch+1
#        else:
#            # if it is a list, it has a sublineage
#            x=[]
#            for i in range(0,2):
#                # for each daughter sublineage, get the id and time interval data
#                sub_lin_id = lin_id[1][i]
#                sub_lin_interval = lin_interval[1][i]
#                # and draw sublineage sublineage
#                (x_curr_branch,x_end_branch) = self.draw_lineage(sub_lin_id, sub_lin_interval,t_end,x_curr_branch,x_end_branch)
#                # for each sublineage, save the current branch x position
#                x.append(x_curr_branch)
#            # get the start of the time interval
#            t0=lin_interval[0]
#            # and the end            
#            if type(lin_interval[1][0])!=list:
#                t1=lin_interval[1][0]
#            else:
#                t1=lin_interval[1][0][0]
#            # plot horizontal line connected the two daughter branches
#            plt.plot([x[0],x[1]], [ t1,t1 ], '-k')
#            # and plot the mother branch
#            x_curr_branch=(x[0]+x[1])/2.
#            plt.plot([x_curr_branch,x_curr_branch], [ t0,t1 ], '-k')
#    
#        # return updated lineage data        
#        return (x_curr_branch,x_end_branch)

    def is_in_lineage(self,lin_id, cell_id):
        if type(lin_id)!=list:
            if lin_id==cell_id:
                return(True)
        else:
            if lin_id[0]==cell_id:
                return(True)
            elif type(lin_id[1])==list:
                for i in range(0,2):
                    if self.is_in_lineage(lin_id[1][i], cell_id):
                        return(True)
            elif lin_id[1]==cell_id:
                    return(True)
                
        return(False)

    # checks if a cell with id=cell_id is in this lineage        
    def is_cell_in_lineage(self, cell_id):
        return ( self.is_in_lineage(self.lin_id, cell_id) )
