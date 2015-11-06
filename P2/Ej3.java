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

public class Ej3 {

    public static class TokenizerMapper 
	extends Mapper<Object, Text, Text, Text>{
	
	public void map(Object key, Text value, Context context
			) throws IOException, InterruptedException {
	    

	    String regex = "[^A-Za-z ]+";
	    String v = value.toString().replaceAll(regex,"");
	    String[] data = v.split(" ");
	    Path filePath = ((FileSplit) context.getInputSplit()).getPath();
	    String filePathString = ((FileSplit) context.getInputSplit()).getPath().toString();
	    String fileName = ((FileSplit) context.getInputSplit()).getPath().getName();
	    for(String w: data)
		if (!w.equals(""))
		    context.write(new Text(w.toLowerCase()),
				  new Text(fileName));


	}
    }
    
 
    public static class IntSumReducer 
	extends Reducer<Text, Text, Text, Text> {

	public void reduce(Text key, Iterable<Text> values, 
			   Context context
			   ) throws IOException, InterruptedException {
	    Map < String,Integer> lib = new HashMap<String,Integer>();

	    boolean mas = false;
	    String opt = "";
	    for (Text val: values) {
		String word = val.toString();
		if(lib.containsKey(word)) {
                    Integer valor = lib.get(word);
                    lib.put(word, valor + 1);
		    if(valor > 19) mas = true;
                }
                else
                    lib.put(word, 1);

	    }

	    Set<Entry<String, Integer>> set = lib.entrySet();
	    List<Entry<String, Integer>> list = new ArrayList<Entry<String, Integer>>(set);
	    Collections.sort( list, new Comparator<Map.Entry<String, Integer>>()
			      {
				  public int compare( Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2 )
				  {
				      return (o2.getValue()).compareTo( o1.getValue() );
				  }
			      } );
	    boolean primero = false;
	    for(Map.Entry<String, Integer> entry:list){
		if(primero)
		    opt+=',';
		primero = true;
		opt += "("+entry.getKey()+","+entry.getValue()+")";
	    }
	    if (mas)
		context.write(key, new Text(opt));
	}
    }



    public static void main(String[] args) throws Exception {
	JobConf conf = new JobConf();
	Job job = Job.getInstance(conf);
	job.setJarByClass(Ej3.class);
	job.setMapperClass(TokenizerMapper.class);
	//Si existe combinador
	//job.setCombinerClass(Clase_del_combinador.class);
	job.setReducerClass(IntSumReducer.class);

	// Declaración de tipos de salida para el mapper
	job.setMapOutputKeyClass(Text.class);
	job.setMapOutputValueClass(Text.class);
	// Declaración de tipos de salida para el reducer
	job.setOutputKeyClass(Text.class);
	job.setOutputValueClass(Text.class);

	// Archivos de entrada y directorio de salida
	FileInputFormat.addInputPath(job, new Path( "data/Adventures_of_Huckleberry_Finn.txt" ));
	FileInputFormat.addInputPath(job, new Path( "data/Hamlet.txt" ));
	FileInputFormat.addInputPath(job, new Path( "data/Moby_Dick.txt" ));
	FileOutputFormat.setOutputPath(job, new Path( "salida" ));
    
	// Aquí podemos elegir el numero de nodos Reduce
	job.setNumReduceTasks(1);

	// Ejecuta la tarea y espera a que termine. El argumento boolean es para 
	// indicar si se quiere información sobre de progreso (verbosity)
	System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

