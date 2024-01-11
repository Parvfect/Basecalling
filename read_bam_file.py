
import bamnostic as bs

bam = bs.AlignmentFile("calls.bam", 'rb')
print(next(bam))
print(bam.head(n=2))