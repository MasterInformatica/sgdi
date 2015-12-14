/**
 Sistemas de gestion de datos y de la informacion 
 Practica 1
 Luis Maria Costero Valero 
 Jesus Javier Domenech Arellano 

 Nosotros, Luis M. Costero y Jesus Domenech, declaramos la autoria completa de este documento. 

La informacion extra no vista en clase ha sido consultada principalmente en
https://hadoop.apache.org/docs/current/api/org/apache/hadoop/io/
 **/

import java.io.IOException;
import java.util.StringTokenizer;

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

public class Ej1 {

    public static class TokenizerMapper 
	extends Mapper<Object, Text, IntWritable, FloatWritable>{
	
	public void map(Object key, Text value, Context context
			) throws IOException, InterruptedException {
	    
	    String[] partes = value.toString().split(",");

	    context.write(new IntWritable(new Integer(partes[2])),
			  new FloatWritable(new Float(partes[8])));
	}
    }
    
 
    public static class IntSumReducer 
	extends Reducer<IntWritable, FloatWritable, IntWritable, Text> {

	public void reduce(IntWritable key, Iterable<FloatWritable> values, 
			   Context context
			   ) throws IOException, InterruptedException {

	    float min = 1e9f;
	    float max = 1e-9f;
	
	
	    for (FloatWritable val: values) {
		if(min > val.get())   min = val.get();
		if(max < val.get())   max = val.get();
	    }
	
	    context.write(key, new Text("("+min+","+max+")"));
	}
    }



    public static void main(String[] args) throws Exception {
	JobConf conf = new JobConf();
	Job job = Job.getInstance(conf);
	job.setJarByClass(Ej1.class);
	job.setMapperClass(TokenizerMapper.class);
	//Si existe combinador
	//job.setCombinerClass(Clase_del_combinador.class);
	job.setReducerClass(IntSumReducer.class);

	// Declaración de tipos de salida para el mapper
	job.setMapOutputKeyClass(IntWritable.class);
	job.setMapOutputValueClass(FloatWritable.class);
	// Declaración de tipos de salida para el reducer
	job.setOutputKeyClass(IntWritable.class);
	job.setOutputValueClass(Text.class);

	// Archivos de entrada y directorio de salida
	FileInputFormat.addInputPath(job, new Path( "data/JCMB_last31days.csv" ));
	FileOutputFormat.setOutputPath(job, new Path( "salida" ));
    
	// Aquí podemos elegir el numero de nodos Reduce
	job.setNumReduceTasks(1);

	// Ejecuta la tarea y espera a que termine. El argumento boolean es para 
	// indicar si se quiere información sobre de progreso (verbosity)
	System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

