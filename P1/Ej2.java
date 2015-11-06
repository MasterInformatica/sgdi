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

public class Ej2 {

    public static class TokenizerMapper 
	extends Mapper<Object, Text, Text, Text>{
	
	public void map(Object key, Text value, Context context
			) throws IOException, InterruptedException {
	    
	    String[] data = value.toString().split("\t");
	    if(new Float(data[2]) < 2 && !data[4].equals("--"))
		context.write(new Text("Triste"),
			      new Text((data[0])));
	}
    }
    
 
    public static class IntSumReducer 
	extends Reducer<Text, Text, IntWritable, Text> {

	public void reduce(Text key, Iterable<Text> values, 
			   Context context
			   ) throws IOException, InterruptedException {

	    int n = 0;
	    String opt = "";
	    for (Text val: values) {
		if (n!=0)
		    opt +=", ";
		n++;
		opt += val.toString();

	    }
	
	    context.write(new IntWritable(n), new Text(opt));
	}
    }



    public static void main(String[] args) throws Exception {
	JobConf conf = new JobConf();
	Job job = Job.getInstance(conf);
	job.setJarByClass(Ej2.class);
	job.setMapperClass(TokenizerMapper.class);
	//Si existe combinador
	//job.setCombinerClass(Clase_del_combinador.class);
	job.setReducerClass(IntSumReducer.class);

	// Declaración de tipos de salida para el mapper
	job.setMapOutputKeyClass(Text.class);
	job.setMapOutputValueClass(Text.class);
	// Declaración de tipos de salida para el reducer
	job.setOutputKeyClass(IntWritable.class);
	job.setOutputValueClass(Text.class);

	// Archivos de entrada y directorio de salida
	FileInputFormat.addInputPath(job, new Path( "data/happiness.txt" ));
	FileOutputFormat.setOutputPath(job, new Path( "salida" ));
    
	// Aquí podemos elegir el numero de nodos Reduce
	job.setNumReduceTasks(1);

	// Ejecuta la tarea y espera a que termine. El argumento boolean es para 
	// indicar si se quiere información sobre de progreso (verbosity)
	System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}

