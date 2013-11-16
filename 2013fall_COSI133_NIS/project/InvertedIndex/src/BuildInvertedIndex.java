import java.io.IOException;
import java.util.*;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;

import edu.umd.cloud9.collection.wikipedia.*;

public class BuildInvertedIndex {

	public static class Map extends MapReduceBase implements Mapper<LongWritable, WikipediaPage, Text, Text> {
		private Text title = new Text();
		private Text word = new Text();

		public void map(LongWritable key, WikipediaPage value, OutputCollector<Text, Text> output, Reporter reporter)
				throws IOException {
			title.set(value.getTitle());
			String content = value.getContent();
			for (String token:StringUtils.split(content)){
				word.set(token);
				output.collect(word,title);
			}
		}
	}

	public static class Reduce extends MapReduceBase implements Reducer<Text, Text, Text, Text> {
		private Text docIds = new Text();
		
		public void reduce(Text key, Iterator<Text> values, OutputCollector<Text, Text> output, Reporter reporter)
				throws IOException {
				HashSet<Text> uniqueDocIds = new HashSet<Text>();
				
				for (;values.hasNext();){
					uniqueDocIds.add(new Text(values.next()));
				}
				
				docIds.set(new Text(StringUtils.join(uniqueDocIds,",")));
				output.collect(key,docIds);
		}


	}

	public static void main(String[] args) throws Exception {

		JobConf conf = new JobConf(BuildInvertedIndex.class);
		
		conf.setInputFormat(WikipediaPageInputFormatOld.class);
		conf.setOutputFormat(TextOutputFormat.class);
		
		conf.setMapperClass(Map.class);
		conf.setReducerClass(Reduce.class);
		
		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(Text.class);
		
		Path outputPath = new Path("output");
		FileInputFormat.addInputPath(conf, new Path("input"));
		FileOutputFormat.setOutputPath(conf, outputPath);
		
		outputPath.getFileSystem(conf).delete(outputPath,true);
		
		JobClient.runJob(conf);
	}

}
