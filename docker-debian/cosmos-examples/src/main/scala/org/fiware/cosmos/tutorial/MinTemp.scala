package org.fiware.cosmos.tutorial
import org.apache.spark._
import org.apache.spark.streaming.{Seconds, StreamingContext}
import org.fiware.cosmos.orion.spark.connector._
/**
  * Minimum temperature Orion Connector
  */
object MinTemp{

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAppName("Example Temp")
    val ssc = new StreamingContext(conf, Seconds(10))
    // Create Orion Receiver. Receive notifications on port 9001
    val eventStream = ssc.receiverStream(new OrionReceiver(9001))

    // Process event stream
    eventStream
      .flatMap(event => event.entities)
      .map(ent => {
        val temp: Float = ent.attrs("temperature").value.asInstanceOf[Number].floatValue()
        (ent.id, temp)
      })
      .reduceByKeyAndWindow(_ min _ ,Seconds(10))

      .print()

    ssc.start()
    ssc.awaitTermination()
  }
}
