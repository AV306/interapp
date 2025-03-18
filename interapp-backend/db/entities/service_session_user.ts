/**
 * Information on a user's participation in an Interact service session.
 * i.e. session ID, username of participant, is ad-hoc, attendance state
 */

import { Entity, PrimaryColumn, Column, ManyToOne, type Relation } from 'typeorm';
import { User } from './user';
import { ServiceSession } from './service_session';

export enum AttendanceStatus {
  Attended = 'Attended',
  Absent = 'Absent',
  ValidReason = 'Valid Reason',
  Late = 'Late' // FIXME: task 1 -- add "late" status; finish the frontend change
}

@Entity()
export class ServiceSessionUser {
  @PrimaryColumn()
  service_session_id: number;

  @PrimaryColumn()
  username: string;

  @Column()
  ad_hoc: boolean;

  @Column({
    type: 'enum',
    enum: AttendanceStatus,
  })
  attended: AttendanceStatus;

  @Column()
  is_ic: boolean;

  @ManyToOne(() => ServiceSession, (service_session) => service_session.service_session_users, {
    onDelete: 'CASCADE',
    onUpdate: 'CASCADE',
  })
  service_session: Relation<ServiceSession>;

  @ManyToOne(() => User, (user) => user.service_session_users, {
    onDelete: 'CASCADE',
    onUpdate: 'CASCADE',
  })
  user: Relation<User>;
}
