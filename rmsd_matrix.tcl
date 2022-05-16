
# Mauricio Bedoya
# maurobedoyat@gmail.com
# Compute RMSD matrix and centroid for a defined cluster of structures.
# execute with
# vmd -dispdev text -e rmsd_matrix.tcl
# If this script is useful for you, consider giving acknowledgments comments in the publication.

#set selection "resname PHA and noh"
#set outfile [open rmsd_matrix.csv w]
#######################################
#set n 8
#for { set i 0 } { $i < $n } { incr i } {
#	###$sel frame $i
#  }
#########################################
#
########## Selection ########
#set selection "protein"
#
#set num_frames [molinfo top get numframes]
#
#for {set fram 0} {$fram < $num_frames} {incr fram } {
#    animate goto $fram
#
#    set sel [atomselect top $selection frame $fram]
#    set a [expr $fram+1]
#    set basename [format "%03d" $a]
#    $sel writepdb "$basename.pdb"
#}
##################################
#
#####################
#set basename1 em1
#
## Trajectory basename
#set basename2 no_modificado_rep1
#
#mol new $basename1.gro type gro first 0 last -1 step 1 filebonds on autobonds on waitfor all
#mol addfile $basename2.trr first 0 last -1 step 1 filebonds on autobonds on waitfor all 
#
#
################################
#
#
#######################
#To to something with the trajectory
#######################
#for {set fram 0} {$fram < $num_frames} {incr fram } {
#    animate goto $fram
#      set actual [atomselect top "$selection" frame $fram]
#    set rms [ measure rmsd $actual $ref ]
#    puts $outfile [format "%s %s" $fram $rms]
#}

##################################
#set selection "resname PHA and noh"
#for { set x 0 } { $x < 8 } { incr x } {
#	puts "x is $x"
	set selection "resname PHA and noh"
	set outfile [open rmsd_matrix_7.csv w]
	
	set filelist [glob ./7_*.pdb]
	puts -nonewline $outfile "EMPTY"
	foreach file $filelist {
	    mol new $file
	    puts -nonewline $outfile ","
	    puts -nonewline $outfile $file
	    
	}
	puts -nonewline $outfile ",average"
	
	#puts [molinfo list]
	
	set rmsav_lower 1000
	set name_lower  0
	set rmsav_name_list {}
	
	#foreach mol [molinfo list] {
	foreach mol [molinfo list] {
	    puts $outfile ""
	    set ref [atomselect $mol "$selection"]
	    set name [molinfo $mol get {filename}]
	    puts -nonewline $outfile $name
	    set rmslist {}
	    foreach mol [molinfo list] {
	        set actual [atomselect $mol "$selection"]
	        set rms [ measure rmsd $actual $ref ]
	        
	        puts -nonewline $outfile ","
	        puts -nonewline $outfile $rms
	        lappend rmslist $rms
	
	    }
	    set rmsav [expr ([join $rmslist +])/[llength $rmslist]]
	    puts -nonewline $outfile ","
	    puts -nonewline $outfile $rmsav
	
	    if {$rmsav <= $rmsav_lower} {
	        set rmsav_lower $rmsav
	        set name_lower $name
	    } else {
	    }
	}
	puts $outfile ""
	puts -nonewline $outfile "the centroid is " 
	puts -nonewline $outfile $name_lower 
	puts -nonewline $outfile " with an average rmsd of " 
	puts -nonewline $outfile $rmsav_lower
	close $outfile
	
	puts ""
	puts -nonewline "the centroid is " 
	puts -nonewline $name_lower 
	puts -nonewline " with an average rmsd of " 
	puts -nonewline $rmsav_lower
	puts ""
	puts ""
	
	exit

