from app.models.payment import Payment
from app.models.customer import Customer
from app.models.file_upload import FileUpload
from app.services.excel_processor import ExcelProcessor
from app.services.analysis_service import AnalysisService
from app import db
from datetime import datetime
import os

class FileService:
    """Handle file upload and processing"""
    
    @staticmethod
    def process_uploaded_file(file_path, original_filename, column_mapping=None):
        """Process uploaded Excel file"""
        try:
            # Read Excel file
            df = ExcelProcessor.read_excel(file_path)
            
            # Auto-detect columns if not provided
            if column_mapping is None:
                column_mapping = ExcelProcessor.detect_columns(df)
            
            # Validate and process data
            processed_data = ExcelProcessor.validate_and_process(df, column_mapping)
            
            # Create FileUpload record
            file_record = FileUpload(
                filename=os.path.basename(file_path),
                original_filename=original_filename,
                file_path=file_path,
                record_count=len(processed_data),
                status='processed'
            )
            db.session.add(file_record)
            db.session.flush()  # Get the id
            
            # Process each record
            for data in processed_data:
                # Get or create customer
                customer = Customer.query.filter_by(name=data['customer_name']).first()
                if not customer:
                    customer = Customer(
                        name=data['customer_name'],
                        email=data['email'],
                        phone=data['phone']
                    )
                    db.session.add(customer)
                    db.session.flush()
                else:
                    # Update customer info
                    if data['email'] and not customer.email:
                        customer.email = data['email']
                    if data['phone'] and not customer.phone:
                        customer.phone = data['phone']
                
                # Create payment record
                status = AnalysisService.determine_status(data['due_date'], data['payment_date'])
                days_late = AnalysisService.calculate_days_late(data['due_date'], data['payment_date'])
                
                payment = Payment(
                    customer_id=customer.id,
                    amount=data['amount'],
                    due_date=data['due_date'],
                    payment_date=data['payment_date'],
                    status=status,
                    days_late=days_late,
                    file_upload_id=file_record.id
                )
                db.session.add(payment)
                
                # Update customer stats
                customer.total_transactions += 1
                customer.total_amount += data['amount']
                if days_late > 0:
                    customer.late_payment_count += 1
                customer.calculate_risk_score()
            
            db.session.commit()
            
            return {
                'success': True,
                'file_id': file_record.id,
                'records_processed': len(processed_data),
                'message': f'Successfully processed {len(processed_data)} records'
            }
        
        except Exception as e:
            db.session.rollback()
            return {
                'success': False,
                'error': str(e),
                'message': f'Failed to process file: {str(e)}'
            }
    
    @staticmethod
    def get_uploaded_files():
        """Get list of all uploaded files"""
        files = FileUpload.query.order_by(FileUpload.upload_date.desc()).all()
        return [f.to_dict() for f in files]
