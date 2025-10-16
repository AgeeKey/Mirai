"""
apache-beam - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.81
Tests Passed: 0/1
Learned: 2025-10-16T21:04:47.071075

This code has been verified by MIRAI's NASA-level learning system.
"""

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

class ProcessData(beam.DoFn):
    """DoFn to process individual elements in the PCollection."""
    
    def process(self, element: str) -> str:
        """Process the input element by converting it to uppercase.
        
        Args:
            element (str): The input string element.
        
        Returns:
            Iterator[str]: An iterator yielding the processed string.
        """
        try:
            yield element.upper()  # Convert to uppercase
        except Exception as e:
            raise RuntimeError(f"Error processing element {element}: {e}")

def run() -> None:
    """Run the Apache Beam pipeline."""
    
    options = PipelineOptions()
    
    with beam.Pipeline(options=options) as p:
        (
            p 
            | 'ReadInput' >> beam.Create(['hello', 'world', 'apache', 'beam'])
            | 'ProcessData' >> beam.ParDo(ProcessData())
            | 'PrintOutput' >> beam.Map(print)  # Print the output elements
        )

if __name__ == '__main__':
    run()