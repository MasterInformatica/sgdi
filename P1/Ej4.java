import java.io.IOException;
import java.util.StringTokenizer;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Writable;
import java.io.DataOutput;
import java.io.DataInput;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;


/** Vector wirtable para pasar los datos **/


public class Ej4 {

    public static class IntVectorWritable implements Writable {
	private Vector<Integer> vector;
    
	public int getElemt(int i){
	    return this.vector.elementAt(i);
	}
	public void insert(int E){
	    if (this.vector == null)
		this.vector = new Vector<Integer>();
	    this.vector.add(E);
	}

	public void IntVectorWritable(){
	    this.vector = new Vector<Integer>();
	}


	public void write(DataOutput out) throws IOException {
	    out.writeInt(this.vector.size());
	    for(int t : this.vector){
		out.writeInt(t);
	    }
	}
    
	public void readFields(DataInput in) throws IOException {
	    int numElems=in.readInt();
	    this.vector = new Vector<Integer>(numElems);
	    for(int i=0; i<numElems; i++){
		this.vector.add(i, in.readInt());
	    }
	}

	public int compareTo(IntVectorWritable v) {
	    if(this.vector.size() != v.vector.size())
		return (this.vector.size() > v.vector.size()) ? 1 : -1;

	    for(int i=0; i<this.vector.size(); i++){
		if(this.vector.elementAt(i) != v.vector.elementAt(i))
		    return (this.vector.elementAt(i) 
			    > v.vector.elementAt(i)) ? 1 : -1;
	    }
	    return 0;
	}
    }


    public static class TokenizerMapper extends Mapper<Object, Text, Text,IntVectorWritable>{
	
	public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
    
	    String v = value.toString();
	    String[] w = v.split(" ");
	    int error = (Integer.parseInt(w[w.length-2]) >= 400 && Integer.parseInt(w[w.length-2]) < 600) ? 1 : 0;
	    int byt = (w[w.length-1].equals("-")) ? 0 : Integer.parseInt(w[w.length-1]);
	    IntVectorWritable ivw = new IntVectorWritable();
	    ivw.insert(byt);
	    ivw.insert(error);
	    context.write(new Text(w[0]), ivw);
	}
    }
    
    public static class OwnCombiner extends Reducer<Text, IntVectorWritable, Text, IntVectorWritable> {

	public void reduce(Text key, Iterable<IntVectorWritable> values, Context context) throws IOException, InterruptedException {

	    int total = 0;
	    int size = 0;
	    int errs = 0;
			
	    for (IntVectorWritable val: values) {
		total++;
		size += val.getElemt(0);
		errs += val.getElemt(1);
	    }
	    IntVectorWritable ivw = new IntVectorWritable();
	    ivw.insert(total);
	    ivw.insert(size);
	    ivw.insert(errs);
	    context.write(key, ivw);
	}
    }
	
 
    public static class IntSumReducer extends Reducer<Text, IntVectorWritable, Text, Text> {
		
	public void reduce(Text key, Iterable<IntVectorWritable> values, Context context) throws IOException, InterruptedException {
	    int total = 0;
	    int size = 0;
	    int errs = 0;

	    for (IntVectorWritable val: values) {
		total+= val.getElemt(0);
		size += val.getElemt(1);
		errs += val.getElemt(2);
	    }
			
	    context.write(key,  new Text("("+total+", "+size+", "+errs+")"));
	}

    }



    public static void main(String[] args) throws Exception {
	JobConf conf = new JobConf();
	Job job = Job.getInstance(conf);
	job.setJarByClass(Ej4.class);
	job.setMapperClass(TokenizerMapper.class);

	//Si existe combinador
	job.setCombinerClass(OwnCombiner.class);
	job.setReducerClass(IntSumReducer.class);

	// Declaración de tipos de salida para el mapper
	job.setMapOutputKeyClass(Text.class);
	job.setMapOutputValueClass(IntVectorWritable.class);
	// Declaración de tipos de salida para el reducer
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(Text.class);

	// Archivos de entrada y directorio de salida
	FileInputFormat.addInputPath(job, new Path( "data/weblog.txt" ));
	FileOutputFormat.setOutputPath(job, new Path( "salida" ));
    
	// Aquí podemos elegir el numero de nodos Reduce
	job.setNumReduceTasks(1);

	// Ejecuta la tarea y espera a que termine. El argumento boolean es para 
	// indicar si se quiere información sobre de progreso (verbosity)
	System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

