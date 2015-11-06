import java.io.IOException;
import java.util.StringTokenizer;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Map.Entry;

import org.apache.hadoop.fs.Path;
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

public class Ej4 {

    public static class TokenizerMapper extends Mapper<Object, Text, Text, Text>{
	
	public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
    
	    String v = value.toString();
	    String[] w = v.split(" ");
	    int error = (Integer.parseInt(w[w.length-2]) >= 400 && Integer.parseInt(w[w.length-2]) < 600) ? 1 : 0;
	    int byt = (w[w.length-1].equals("-")) ? 0 : Integer.parseInt(w[w.length-1]);
	    context.write(new Text(w[0]),  new Text(""+byt+","+error));
	}
    }
    
    public static class OwnCombiner extends Reducer<Text, Text, Text, Text> {

	public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

	    int total = 0;
	    int size = 0;
	    int errs = 0;
			
	    for (Text val: values) {
		String[] str = val.toString().split(",");
		total++;
		size += Integer.parseInt(str[0]);
		errs += Integer.parseInt(str[1]);
	    }
			
	    context.write(key,  new Text(""+total+","+size+","+errs));
	
	}
    }
	
 
    public static class IntSumReducer extends Reducer<Text, Text, Text, Text> {
		
	public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
	    int total = 0;
	    int size = 0;
	    int errs = 0;
			
	    for (Text val: values) {
		String[] str = val.toString().split(",");
		total+= Integer.parseInt(str[0]);
		size += Integer.parseInt(str[1]);
		errs += Integer.parseInt(str[2]);
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
	job.setMapOutputValueClass(Text.class);
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

